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
"""Grok components"""

from operator import itemgetter

from zope import component, interface
from zope.viewlet.manager import ViewletManagerBase
from zope.viewlet.viewlet import ViewletBase

from grokcore.viewlet import interfaces, util


class ViewletManager(ViewletManagerBase):
    interface.implements(interfaces.IViewletManager)

    template = None

    def __init__(self, context, request, view):
        super(ViewletManager, self).__init__(context, request, view)
        self.context = context
        self.request = request
        self.view = view
        self.__name__ = self.__view_name__
        static_name = getattr(self, '__static_name__', None)
        if static_name is not None:
            self.static = component.queryAdapter(
                self.request,
                interface.Interface,
                name=static_name)
        else:
            self.static = None

    def sort(self, viewlets):
        """Sort the viewlets.

        ``viewlets`` is a list of tuples of the form (name, viewlet).
        """
        # Sort viewlets following grok.order rule.
        return util.sort_components(viewlets, key=itemgetter(1))

    def default_namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['static'] = self.static
        namespace['view'] = self.view
        namespace['viewletmanager'] = self
        return namespace

    def namespace(self):
        return {}

    def update(self):
        super(ViewletManager, self).update()
        # Filter out the unavailable viewlets *after* the viewlet's update()
        # has been called.
        self.viewlets = filter(lambda v: v.available(), self.viewlets)

    def render(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        # Now render the view
        if self.template:
            return self.template.render(self)
        else:
            return u'\n'.join([viewlet.render() for viewlet in self.viewlets])
    # Mark the render() method as a method from the base class. That
    # way we can detect whether somebody overrides render() in a subclass.
    render.base_method = True


class Viewlet(ViewletBase):
    """Batteries included viewlet.
    """

    def __init__(self, context, request, view, manager):
        super(Viewlet, self).__init__(context, request, view, manager)
        self.context = context
        self.request = request
        self.view = view
        self.viewletmanager = manager
        self.__name__ = self.__view_name__
        static_name = getattr(self, '__static_name__', None)
        if static_name is not None:
            self.static = component.queryAdapter(
                self.request,
                interface.Interface,
                name=static_name)
        else:
            self.static = None

    def default_namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['static'] = self.static
        namespace['view'] = self.view
        namespace['viewlet'] = self
        namespace['viewletmanager'] = self.manager
        return namespace

    def namespace(self):
        return {}

    def update(self):
        pass

    def available(self):
        """Return True if this viewlet is to be rendered. False otherwise.

        Note that the available() method is called *after* update() but
        *before* render() has been called.
        """
        return True

    def render(self):
        return self.template.render(self)
    # Mark the render() method as a method from the base class. That
    # way we can detect whether somebody overrides render() in a subclass.
    render.base_method = True
