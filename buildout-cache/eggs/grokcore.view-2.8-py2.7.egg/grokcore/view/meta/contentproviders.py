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
"""Grokkers for the views code."""
from zope import component
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import martian

import grokcore.security
import grokcore.view
from grokcore.view.interfaces import IContentProvider
from grokcore.view.meta.views import default_view_name, TemplateGrokker


class ContentProviderTemplateGrokker(TemplateGrokker):
    martian.component(grokcore.view.ContentProvider)


class ContentProviderGrokker(martian.ClassGrokker):
    martian.component(grokcore.view.ContentProvider)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.view.view)
    martian.directive(grokcore.component.name, get_default=default_view_name)

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the view class so that it
        # can look up the 'static' resource directory.
        factory.module_info = module_info
        return super(ContentProviderGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, context, layer, view, name, **kw):
        # This will be used to support __name__ on the viewlet manager
        factory.__view_name__ = name

        config.action(
            discriminator=('contentprovider', context, layer, view, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, (context, layer, view), IContentProvider, name))
        return True



