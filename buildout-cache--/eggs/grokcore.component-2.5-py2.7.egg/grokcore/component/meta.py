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

import operator

import martian
import martian.util
import grokcore.component
import zope.component.interface
from zope import component, interface
from martian.error import GrokError
from zope.interface import implementedBy

def _provides(component, module=None, **data):
    martian.util.check_implements_one(component)
    return list(interface.implementedBy(component))[0]

def default_global_utility_provides(component, module, direct, **data):
    if direct:
        martian.util.check_provides_one(component)
        return list(interface.providedBy(component))[0]
    return _provides(component)


class AdapterGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.Adapter)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.component.provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, context, provides, name, **kw):
        config.action(
            discriminator=('adapter', context, provides, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, (context,), provides, name),
            )
        return True


class MultiAdapterGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.MultiAdapter)
    martian.directive(grokcore.component.provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, provides, name, **kw):
        for_ = component.adaptedBy(factory)
        if for_ is None:
            raise GrokError("%r must specify which contexts it adapts "
                            "(use the 'adapts' directive to specify)."
                            % factory, factory)

        config.action(
            discriminator=('adapter', for_, provides, name),
            callable=grokcore.component.provideAdapter,
            args=(factory, None, provides, name),
            )
        return True


class SubscriptionGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.Subscription)
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.component.provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, context, provides, name, **kw):
        config.action(
            discriminator=None,
            callable=grokcore.component.provideSubscriptionAdapter,
            args=(factory, (context,), provides),
            )
        return True


class MultiSubscriptionGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.MultiSubscription)
    martian.directive(grokcore.component.provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, provides, name, **kw):
        adapts = component.adaptedBy(factory)
        if adapts is None:
            raise GrokError("%r must specify which contexts it adapts "
                            "(use the 'adapts' directive to specify)."
                            % factory, factory)

        config.action(
            discriminator=None,
            callable=grokcore.component.provideSubscriptionAdapter,
            args=(factory, adapts, provides),
            )
        return True


class GlobalUtilityGrokker(martian.ClassGrokker):
    martian.component(grokcore.component.GlobalUtility)

    # This needs to happen before the FilesystemPageTemplateGrokker grokker
    # happens, since it relies on the ITemplateFileFactories being grokked.
    martian.priority(1100)

    martian.directive(grokcore.component.direct)
    martian.directive(grokcore.component.provides,
                      get_default=default_global_utility_provides)
    martian.directive(grokcore.component.name)

    def execute(self, factory, config, direct, provides, name, **kw):
        if not direct:
            factory = factory()

        config.action(
            discriminator=('utility', provides, name),
            callable=grokcore.component.provideUtility,
            args=(factory, provides, name),
            )
        return True


class ImplementerDecoratorGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        adapters = module_info.getAnnotation('grok.adapters', [])
        subscribers = set(map(operator.itemgetter(0),
                              module_info.getAnnotation('grok.subscribers', [])))

        for function in adapters:
            if function in subscribers:
                # We don't register functions that are decorated with
                # grok.implementer() *and* the grok.subscribe()
                # decorator. These are registered as so called
                # subcribers and not as regular adapters.
                continue
            interfaces = getattr(function, '__component_adapts__', None)
            if interfaces is None:
                context = grokcore.component.context.bind().get(module)
                interfaces = (context, )
            name = getattr(function, '__component_name__', u"")
            config.action(
                discriminator=('adapter', interfaces, function.__implemented__, name),
                callable=grokcore.component.provideAdapter,
                args=(function, interfaces, function.__implemented__, name),
                )
        return True

class GlobalUtilityDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        infos = grokcore.component.global_utility.bind().get(module)

        for factory, provides, name, direct in infos:
            if direct is None:
                direct = grokcore.component.direct.bind().get(factory)
            if provides is None:
                bound = grokcore.component.provides.bind(default=None)
                provides = bound.get(factory)
            if not name:
                name = grokcore.component.name.bind().get(factory)

            if direct:
                obj = factory
                if provides is None:
                    martian.util.check_provides_one(obj)
                    provides = list(interface.providedBy(obj))[0]
            else:
                obj = factory()
                if provides is None:
                    provides = _provides(factory)

            config.action(
                discriminator=('utility', provides, name),
                callable=grokcore.component.provideUtility,
                args=(obj, provides, name),
                )

        return True


class GlobalAdapterDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        infos = grokcore.component.global_adapter.bind().get(module)
        for factory, adapts, provides, name in infos:
            if provides is None:
                bound = grokcore.component.provides.bind(default=None)
                provides = bound.get(factory)
            if adapts is None:
                adapts = (grokcore.component.context.bind().get(module),)
            if name is None:
                name = grokcore.component.name.bind().get(factory)

            config.action(
                discriminator=('adapter', adapts, provides, name),
                callable=grokcore.component.provideAdapter,
                args=(factory, adapts, provides, name),
                )

        return True


class SubscriberDirectiveGrokker(martian.GlobalGrokker):

    def grok(self, name, module, module_info, config, **kw):
        subscribers = module_info.getAnnotation('grok.subscribers', [])

        for factory, subscribed in subscribers:
            provides = None
            implemented = list(implementedBy(factory))
            if len(implemented) == 1:
                provides = implemented[0]
            # provideHandler is essentially the same as
            # provideSubscriptionAdapter, where provided=None. However,
            # handlers and subscription adapters are tracked in
            # separately so we cannot exchange one registration call
            # for the the other.
            if provides is None:
                config.action(
                    discriminator=None,
                    callable=grokcore.component.provideHandler,
                    args=(factory, subscribed))
            else:
                config.action(
                    discriminator=None,
                    callable=grokcore.component.provideSubscriptionAdapter,
                    args=(factory, subscribed, provides))

            for iface in subscribed:
                config.action(
                    discriminator=None,
                    callable=grokcore.component.provideInterface,
                    args=('', iface))
        return True
