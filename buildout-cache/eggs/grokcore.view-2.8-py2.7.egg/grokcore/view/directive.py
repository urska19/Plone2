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
import os.path
import sys

import martian
from martian.error import GrokImportError
from martian.directive import StoreOnce
from zope.interface.interface import TAGGED_DATA
from zope.publisher.interfaces.browser import IBrowserView


def validateLocalPath(directive, value):
    martian.validateText(directive, value)
    if os.path.sep in value:
        raise GrokImportError(
            "The '%s' directive can not contain path separator."
            % directive.name)
    # XXX kinda hackish...
    dirname = os.path.dirname(directive.frame.f_locals['__file__'])
    if not os.path.isdir(os.path.join(dirname, value)):
        raise GrokImportError(
            "The directory '%s' specified by the '%s' directive "
            "cannot be found." % (value, directive.name))

# Define grok directives


class template(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

    def factory(self, name):
        # In combination of the name, store from which module the
        # template is refered.
        f_locals = sys._getframe(2).f_locals
        return (f_locals['__module__'], name)


class templatedir(martian.Directive):
    scope = martian.MODULE
    store = martian.ONCE
    validate = validateLocalPath


class OneInterfaceOrClassOnClassOrModule(martian.Directive):
    """Convenience base class.  Not for public use."""
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass


class layer(OneInterfaceOrClassOnClassOrModule):
    pass


class TaggedValueStoreOnce(StoreOnce):
    """Stores the directive value in a interface tagged value.
    """

    def get(self, directive, component, default):
        return component.queryTaggedValue(directive.dotted_name(), default)

    def set(self, locals_, directive, value):
        already_set = locals_.get('__interface_tagged_values__', [])
        if directive.dotted_name() in already_set:
            raise GrokImportError(
                "The '%s' directive can only be called once per %s." %
                (directive.name, directive.scope.description))
        # Make use of the implementation details of interface tagged
        # values.  Instead of being able to call "setTaggedValue()"
        # on an interface object, we only have access to the "locals"
        # of the interface object.  We inject whatever setTaggedValue()
        # would've injected.
        taggeddata = locals_.setdefault(TAGGED_DATA, {})
        taggeddata[directive.dotted_name()] = value

    def setattr(self, context, directive, value):
        context.setTaggedValue(directive.dotted_name(), value)


class skin(martian.Directive):
    # We cannot do any better than to check for a class scope. Ideally we
    # would've checked whether the context is indeed an Interface class.
    scope = martian.CLASS
    store = TaggedValueStoreOnce()
    validate = martian.validateText


class path(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText

class view(OneInterfaceOrClassOnClassOrModule):
    default = IBrowserView
