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
import sys
import martian
import grokcore.component
from martian import util
from martian.error import GrokImportError, GrokError
from martian.directive import StoreMultipleTimes
from grokcore.security import components

class RequireDirectiveStore(StoreMultipleTimes):

    def get(self, directive, component, default):
        permissions = getattr(component, directive.dotted_name(), default)
        if (permissions is default) or not permissions:
            return default
        if len(permissions) > 1:
            raise GrokError(
                'grok.require was called multiple times in '
                '%r. It may only be set once for a class.'
                % component, component)
        return permissions[0]

    def pop(self, locals_, directive):
        return locals_[directive.dotted_name()].pop()

class require(martian.Directive):
    scope = martian.CLASS
    store = RequireDirectiveStore()

    def validate(self, value):
        if util.check_subclass(value, components.Permission):
            return
        if util.not_unicode_or_ascii(value):
            raise GrokImportError(
                "You can only pass unicode, ASCII, or a subclass "
                "of grok.Permission to the '%s' directive." % self.name)

    def factory(self, value):
        if util.check_subclass(value, components.Permission):
            return grokcore.component.name.bind().get(value)
        return value

    def __call__(self, func):
        # grok.require can be used both as a class-level directive and
        # as a decorator for methods.  Therefore we return a decorator
        # here, which may be used for methods, or simply ignored when
        # used as a directive.
        frame = sys._getframe(1)
        permission = self.store.pop(frame.f_locals, self)
        self.set(func, [permission])
        return func

class permissions(martian.Directive):
    """The `grokcore.security.permissions()` directive.

    This directive is used inside of a `grok.Role` subclass to list the
    permissions which each member of the role should always possess.
    Note that permissions should be passed as strings, and that several
    permissions they can simply be supplied as multiple arguments; there
    is no need to place them inside of a tuple or list::

        class MyRole(grokcore.security.Role):
            grokcore.security.permissions('page.CreatePage', 'page.EditPage')
            ...

    """
    scope = martian.CLASS
    store = martian.ONCE
    default = []

    def validate(self, *values):
        for value in values:
            if martian.util.check_subclass(value, components.Permission):
                continue
            if martian.util.not_unicode_or_ascii(value):
                raise GrokImportError(
                    "You can only pass unicode values, ASCII values, or "
                    "subclasses of grok.Permission to the '%s' directive."
                    % self.name)

    def factory(self, *values):
        permission_ids = []
        for value in values:
            if martian.util.check_subclass(value, components.Permission):
                permission_ids.append(grokcore.component.name.bind().get(value))
            else:
                permission_ids.append(value)
        return permission_ids
