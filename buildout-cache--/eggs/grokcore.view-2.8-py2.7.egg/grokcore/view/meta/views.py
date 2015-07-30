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
import sys

from zope import interface, component
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.publisher.interfaces.browser import IBrowserPage

import martian
from martian.error import GrokError
from martian import util

import grokcore.security
import grokcore.view
from grokcore.security.util import protect_getattr
from grokcore.view import components
from grokcore.view import templatereg

def default_view_name(component, module=None, **data):
    return component.__name__.lower()


class TemplateGrokker(martian.ClassGrokker):
    martian.baseclass()

    _template_order = sys.maxint/2

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info to look for a template
        factory.module_info = module_info
        return super(TemplateGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, **kw):
        # Associate templates to a view or a component. We set the
        # configuration action order to a number quite high, to do it
        # after all templates have be registered to the shared template
        # registry, and yet before unassociated templates are checked.
        config.action(
            discriminator=None,
            callable=self.associate_template,
            args=(factory.module_info, factory),
            order=self._template_order
            )
        # We increase _template_order to maintain the relative order of
        # template association between the different Grok extensions
        # (like an implicit template can be inherited between two
        # different Grok extensions).
        self._template_order += 1
        return True

    def associate_template(self, module_info, factory):
        component_name = martian.component.bind().get(self).__name__.lower()
        templatereg.associate_template(
            module_info, factory, component_name,
            self.has_render, self.has_no_render)

    def has_render(self, factory):
        render = getattr(factory, 'render', None)
        base_method = getattr(render, 'base_method', False)
        return render and not base_method

    def has_no_render(self, factory):
        return not self.has_render(factory)


class ViewTemplateGrokker(TemplateGrokker):
    martian.component(components.View)


class ViewGrokker(martian.ClassGrokker):
    martian.component(components.View)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)
    martian.directive(grokcore.component.provides, default=interface.Interface)
    martian.directive(grokcore.component.name, get_default=default_view_name)

    def execute(self, factory, config, context, layer, provides, name, **kw):
        # safety belt: make sure that the programmer didn't use
        # @grok.require on any of the view's methods.
        methods = util.methods_from_class(factory)
        for method in methods:
            if grokcore.security.require.bind().get(method) is not None:
                raise GrokError('The @grok.require decorator is used for '
                                'method %r in view %r. It may only be used '
                                'for XML-RPC methods.'
                                % (method.__name__, factory), factory)

        # __view_name__ is needed to support IAbsoluteURL on views
        factory.__view_name__ = name
        adapts = (context, layer)

        config.action(
            discriminator=('adapter', adapts, provides, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, adapts, provides, name),
            )
        return True


class ViewSecurityGrokker(martian.ClassGrokker):
    martian.component(components.View)
    martian.directive(grokcore.security.require, name='permission')

    def execute(self, factory, config, permission, **kw):
        for method_name in IBrowserPage:
            config.action(
                discriminator=('protectName', factory, method_name),
                callable=protect_getattr,
                args=(factory, method_name, permission),
                )
        return True
