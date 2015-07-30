##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok directives.
"""
import martian
import martian.util
from martian.error import GrokError, GrokImportError
from martian.util import scan_for_classes
from zope import interface
from zope.interface.interfaces import IInterface
from grokcore.component.interfaces import IContext

class global_utility(martian.MultipleTimesDirective):
    """Registers an instance of ``class`` (or ``class`` itself, depending on
    the value of the ``direct`` parameter) as a global utility.

    This allows you to register global utilities that don't inherit from the
    ``GlobalUtility`` base class.

    :param class: The class to register as a global utility.
    :param provides: Optionally, the interface the utility will provide.
    :param name: Optionally, a name for a named utility registration.
    :type name: string or unicode
    :param direct: Optionally, a flag indicating the class directly provides
                   the interfaces, and it needs not to be instantiated.
    :type direct: boolean
    """
    scope = martian.MODULE

    def factory(self, factory, provides=None, name=u'', direct=False):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)
        return (factory, provides, name, direct)

class global_adapter(martian.MultipleTimesDirective):
    """Registers the ``factory`` callable as a global adapter.

    This allows you to register global adapters that
    don't inherit from the ``Adapter`` or ``MultiAdapter`` base classes.

    :param factory: The class that implements the adaptation.
    :param adapts: Optionally, a single interface or a tuple of multiple
                   interfaces to adapts from. If omitted, this information is
                   deduced from the annotation on the factory. If no adapted
                   interface can be determined the current context will be
                   assumed.
    :param provides: Optionally, the interface the adapter will provide. If
                     omitted, this information is deduced from the annotations
                     on the factory.
    :param name: Optionally, a name for a named adapter registration.
    :type name: string or unicode

    """
    scope = martian.MODULE

    def factory(self, factory, adapts=None, provides=None, name=None):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)
        if adapts is None:
            adapts = getattr(factory, '__component_adapts__', None)
        elif not isinstance(adapts, (list, tuple,)):
            adapts = (adapts,)
        elif isinstance(adapts, list):
            adapts = tuple(adapts)

        return (factory, adapts, provides, name)

class name(martian.Directive):
    """Declares the name of a named utility, named adapter, etc.

    """
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText
    default = u''

class context(martian.Directive):
    """Declares the type of object that the adapter (or a similar context-
    dependent component) adapts.

    :param context: Interface (in this case all objects providing this
                    interface will be eligible contexts for the adaptation) or
                    a class (then only instances of that particular class are
                    eligible).
    """

    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass

    @classmethod
    def get_default(cls, component, module=None, **data):
        components = list(scan_for_classes(module, IContext))
        if len(components) == 0:
            raise GrokError(
                "No module-level context for %r, please use the 'context' "
                "directive." % (component), component)
        elif len(components) == 1:
            component = components[0]
        else:
            raise GrokError(
                "Multiple possible contexts for %r, please use the 'context' "
                "directive."
                % (component), component)
        return component

class title(martian.Directive):
    """Declares the human-readable title of a component (such as a permission,
    role, etc.)

    """
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class description(title):
    pass

class direct(martian.MarkerDirective):
    """Declares that a ``GlobalUtility`` class should be registered as a
    utility itself, rather than an instance of it.

    """
    scope = martian.CLASS

class order(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    default = 0, 0

    _order = 0

    def factory(self, value=0):
        order._order += 1
        return value, order._order

class path(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class provides(martian.Directive):
    """Declares the interface that a adapter or utility provides for the
    registration, as opposed to potentially multiple interfaces that the class
    implements.

    :param interface: The interface the registered component will provide.

    """
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface

    @classmethod
    def get_default(cls, component, module, **data):
        martian.util.check_implements_one(component)
        return list(interface.implementedBy(component))[0]
