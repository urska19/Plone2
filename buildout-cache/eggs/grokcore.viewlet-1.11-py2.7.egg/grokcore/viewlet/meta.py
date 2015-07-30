#############################################################################
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
"""Grokkers for the various components."""

from zope import component
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.viewlet.interfaces import IViewletManager, IViewlet

import martian

import grokcore.component
import grokcore.view
from grokcore.view.meta.views import default_view_name, TemplateGrokker
import grokcore.security
import grokcore.viewlet
from grokcore.viewlet import components
from grokcore.viewlet.util import make_checker


class ViewletManagerTemplateGrokker(TemplateGrokker):
    martian.component(grokcore.viewlet.ViewletManager)

    def has_render(self, factory):
        render = getattr(factory, 'render', None)
        base_method = getattr(render, 'base_method', False)
        return render and not base_method

    def has_no_render(self, factory):
        # always has a render method
        return False


class ViewletManagerGrokker(martian.ClassGrokker):
    martian.component(grokcore.viewlet.ViewletManager)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.viewlet.view)
    martian.directive(grokcore.component.name, get_default=default_view_name)

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(ViewletManagerGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, context, layer, view, name, **kw):
        # This will be used to support __name__ on the viewlet manager
        factory.__view_name__ = name

        config.action(
            discriminator=('viewletManager', context, layer, view, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, (context, layer, view), IViewletManager, name))
        return True


class ViewletTemplateGrokker(TemplateGrokker):
    martian.component(grokcore.viewlet.Viewlet)

    def has_render(self, factory):
        render = getattr(factory, 'render', None)
        base_method = getattr(render, 'base_method', False)
        return render and not base_method

    def has_no_render(self, factory):
        return not self.has_render(factory)

class ViewletGrokker(martian.ClassGrokker):
    martian.component(grokcore.viewlet.Viewlet)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.viewlet.view)
    martian.directive(grokcore.viewlet.viewletmanager)
    martian.directive(grokcore.component.name, get_default=default_view_name)
    martian.directive(grokcore.security.require, name='permission')

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(ViewletGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config,
                context, layer, view, viewletmanager, name, permission, **kw):
        # This will be used to support __name__ on the viewlet
        factory.__view_name__ = name

        config.action(
            discriminator=(
                'viewlet', context, layer, view, viewletmanager, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, (context, layer, view, viewletmanager),
                  IViewlet, name))

        config.action(
            discriminator=('protectName', factory, '__call__'),
            callable=make_checker,
            args=(factory, factory, permission, ['update', 'render']))

        return True
