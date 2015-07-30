##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
"""Grok
"""
import sys
import types
import zope.component
import zope.interface
from martian.util import frame_is_module
from martian.error import GrokImportError

from zope.interface.declarations import DescriptorAwareMetaClasses

class subscribe:
    """Declares that a function is to be registered as an event handler for the
    specified objects.

    Normally, an event handler is simply registered as a subscriber for the
    event interface. In case of object events, the event handler is registered
    as a subscriber for the object type and the event interface.

    """
    def __init__(self, *args):
        self.subscribed = args

    def __call__(self, function):
        frame = sys._getframe(1)
        if not frame_is_module(frame):
            raise GrokImportError("@grok.subscribe can only be used on module "
                                  "level.")

        if not self.subscribed:
            raise GrokImportError("@grok.subscribe requires at least one "
                                  "argument.")

        # Add the function and subscribed interfaces to the
        # grok.subscribers module annotation.
        subscribers = frame.f_locals.get('__grok_subscribers__', None)
        if subscribers is None:
            frame.f_locals['__grok_subscribers__'] = subscribers = []
        subscribers.append((function, self.subscribed))

        # Also store the subscribed interfaces on the
        # attribute__component_adapts__ for provideHandler to register
        # the subscriber (in case you don't grok your package and
        # register it manually)
        return zope.component.adapter(*self.subscribed)(function)

class adapter(zope.component.adapter):
    """Registers the function as an adapter for the specific interface.

    The ``name`` argument must be a keyword argument and is optional. If given,
    a named adapter is registered.
    """

    # Override the z.c.adapter decorator to force sanity checking and
    # have better error reporting and add the ability to capture the name

    def __init__(self, *interfaces, **kw):
        if not interfaces:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")
        if type(interfaces[0]) is types.FunctionType:
            raise GrokImportError(
                "@grok.adapter requires at least one argument.")

        self.name = u""

        if kw:
            if 'name' in kw:
                self.name = kw.pop('name')
            if kw:
                raise GrokImportError(
                    "@grok.adapter got unexpected keyword arguments: %s" % ','.join(kw.keys()))

        zope.component.adapter.__init__(self, *interfaces)

    def __call__(self, ob):
        ob = zope.component.adapter.__call__(self, ob)
        if self.name:
            ob.__component_name__ = self.name
        return ob

class implementer(zope.interface.implementer):
    """Declares that the function implements a certain interface (or a number
    of interfaces).

    This is useful when a function serves as an object factory, e.g. as an
    adapter.

    """

    def __call__(self, ob):
        # XXX we do not have function grokkers (yet) so we put the annotation
        # on the module.
        frame = sys._getframe(1)
        adapters = frame.f_locals.get('__grok_adapters__', None)
        if adapters is None:
            frame.f_locals['__grok_adapters__'] = adapters = []
        adapters.append(ob)

        return zope.interface.implementer.__call__(self, ob)

class provider:
    """Declares that the function object provides a certain interface (or a
    number of interfaces).

    This is akin to calling directlyProvides() on the function object.

    """
    def __init__(self, *interfaces):
        self.interfaces = interfaces

    def __call__(self, ob):
        if isinstance(ob, DescriptorAwareMetaClasses):
            raise TypeError("Can't use implementer with classes.  Use one of "
                            "the class-declaration functions instead."
                            )
        zope.interface.alsoProvides(ob, *self.interfaces)
        return ob
