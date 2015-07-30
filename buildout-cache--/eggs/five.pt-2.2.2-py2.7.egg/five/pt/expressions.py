from ast import NodeTransformer
from types import ClassType
from compiler import parse as ast24_parse

from OFS.interfaces import ITraversable
from zExceptions import NotFound, Unauthorized

from zope.component import queryMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.contentprovider.interfaces import ContentProviderLookupError
from zope.contentprovider.tales import addTALNamespaceData

try:
    from zope.contentprovider.interfaces import BeforeUpdateEvent
except ImportError:
    BeforeUpdateEvent = None

from zope.event import notify
from zope.location.interfaces import ILocation
from zope.traversing.adapters import traversePathElement
from zope.traversing.interfaces import TraversalError

from RestrictedPython.RestrictionMutator import RestrictionMutator
from RestrictedPython.Utilities import utility_builtins
from RestrictedPython import MutatingWalker

from Products.PageTemplates.Expressions import render

from AccessControl.ZopeGuards import guarded_getattr
from AccessControl.ZopeGuards import guarded_getitem
from AccessControl.ZopeGuards import guarded_apply
from AccessControl.ZopeGuards import guarded_iter
from AccessControl.ZopeGuards import protected_inplacevar

from chameleon.astutil import Symbol
from chameleon.astutil import Static
from chameleon.codegen import template
from sourcecodegen import generate_code

from z3c.pt import expressions

_marker = object()

try:
    # If this import succeeds, we need to use a content provider
    # renderer which acquisition-wraps the provider component
    from Products.Five.browser import providerexpression
    providerexpression

except ImportError:
    ProviderExpr = expressions.ProviderExpr
else:
    def render_content_provider(econtext, name):
        name = name.strip()

        context = econtext.get('context')
        request = econtext.get('request')
        view = econtext.get('view')

        cp = queryMultiAdapter(
            (context, request, view), IContentProvider, name=name)

        # provide a useful error message, if the provider was not found.
        if cp is None:
            raise ContentProviderLookupError(name)

        # add the __name__ attribute if it implements ILocation
        if ILocation.providedBy(cp):
            cp.__name__ = name

        # Insert the data gotten from the context
        addTALNamespaceData(cp, econtext)

        # BBB: This is where we're different:
        if getattr(cp, '__of__', None) is not None:
            cp = cp.__of__(context)

        # Stage 1: Do the state update.
        if BeforeUpdateEvent is not None:
            notify(BeforeUpdateEvent(cp, request))
        cp.update()

        # Stage 2: Render the HTML content.
        return cp.render()

    class ProviderExpr(expressions.ProviderExpr):
        transform = Symbol(render_content_provider)


zope2_exceptions = NameError, \
                   ValueError, \
                   AttributeError, \
                   LookupError, \
                   TypeError, \
                   NotFound, \
                   Unauthorized, \
                   TraversalError


def static(obj):
    return Static(template("obj", obj=Symbol(obj), mode="eval"))


class BoboAwareZopeTraverse(object):
    traverse_method = 'restrictedTraverse'

    __slots__ = ()

    @classmethod
    def traverse(cls, base, request, path_items):
        """See ``zope.app.pagetemplate.engine``."""

        length = len(path_items)
        if length:
            i = 0
            method = cls.traverse_method
            while i < length:
                name = path_items[i]
                i += 1

                if ITraversable.providedBy(base):
                    traverser = getattr(base, method)
                    base = traverser(name)
                else:
                    base = traversePathElement(
                        base, name, path_items[i:], request=request
                        )

        return base

    def __call__(self, base, econtext, call, path_items):
        request = econtext.get('request')

        if path_items:
            base = self.traverse(base, request, path_items)

        if call is False:
            return base

        if getattr(base, '__call__', _marker) is not _marker or callable(base):
            base = render(base, econtext)

        return base


class TrustedBoboAwareZopeTraverse(BoboAwareZopeTraverse):
    traverse_method = 'unrestrictedTraverse'

    __slots__ = ()

    def __call__(self, base, econtext, call, path_items):
        request = econtext.get('request')

        base = self.traverse(base, request, path_items)

        if call is False:
            return base

        if (getattr(base, '__call__', _marker) is not _marker \
            or isinstance(base, ClassType)):
            return base()

        return base


class PathExpr(expressions.PathExpr):
    exceptions = zope2_exceptions

    traverser = Static(template(
        "cls()", cls=Symbol(BoboAwareZopeTraverse), mode="eval"
        ))


class TrustedPathExpr(PathExpr):
    traverser = Static(template(
        "cls()", cls=Symbol(TrustedBoboAwareZopeTraverse), mode="eval"
        ))


class NocallExpr(expressions.NocallExpr, PathExpr):
    pass


class ExistsExpr(expressions.ExistsExpr):
    exceptions = zope2_exceptions


class RestrictionTransform(NodeTransformer):
    secured = {
        '_getattr_': guarded_getattr,
        '_getitem_': guarded_getitem,
        '_apply_': guarded_apply,
        '_getiter_': guarded_iter,
        '_inplacevar_': protected_inplacevar,
    }

    def visit_Name(self, node):
        value = self.secured.get(node.id)
        if value is not None:
            return Symbol(value)

        return node


class UntrustedPythonExpr(expressions.PythonExpr):
    rm = RestrictionMutator()
    rt = RestrictionTransform()

    # Make copy of parent expression builtins
    builtins = expressions.PythonExpr.builtins.copy()

    # Update builtins with Restricted Python utility builtins
    builtins.update(dict(
        (name, static(builtin)) for (name, builtin) in utility_builtins.items()
        ))

    def rewrite(self, node):
        if node.id == 'repeat':
            node.id = 'wrapped_repeat'
        else:
            node = super(UntrustedPythonExpr, self).rewrite(node)

        return node

    def parse(self, string):
        encoded = string.encode('utf-8')
        node = ast24_parse(encoded, 'eval').node
        MutatingWalker.walk(node, self.rm)
        string = generate_code(node)
        decoded = string.decode('utf-8')
        value = super(UntrustedPythonExpr, self).parse(decoded)

        # Run restricted python transform
        self.rt.visit(value)

        return value
