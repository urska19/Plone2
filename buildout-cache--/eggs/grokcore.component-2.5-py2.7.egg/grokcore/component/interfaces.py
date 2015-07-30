##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
"""Public interfaces.
"""
from zope.interface import Interface, Attribute

class IContext(Interface):
    """Marker interface for auto-association of context.

    The ``grok.context()`` directive is used to associate adapters with the
    class or interface they adapt. If there is only a single possible context
    object to adapt to in a module, you can leave out this directive and
    let the adapter associate automatically.

    If you want to make an object to be a candidate for this automatic
    association, you can subclass from ``grokcore.component.Context``.
    This implements this ``IContext`` directive.

    In some cases, you don't want to mix in a base class. You can instead
    mark up your class with ``zope.interface.implements(IContext)`` to make
    it a candidate for auto-association.
    """


class IBaseClasses(Interface):
    Adapter = Attribute("Base class for adapters.")

    ClassGrokker = Attribute("Base class to define a class grokker.")

    Context = Attribute("Base class for automatically associated contexts.")

    GlobalGrokker = Attribute("Base class to define a module grokker.")

    GlobalUtility = Attribute("Base class for global utilities.")

    InstanceGrokker = Attribute("Base class to define an instance grokker.")

    MultiAdapter = Attribute("Base class for multi-adapters.")

    MultiSubscription = Attribute(
        "Base class for subscription mult-adapters.")

    Subscription = Attribute("Base class for subscription adapters.")


class IDirectives(Interface):

    def baseclass():
        """Mark this class as a base class.

        This means it won't be grokked, though if it's a possible context,
        it can still serve as a context.
        """

    def implements(*interfaces):
        """Declare that a class implements the given interfaces."""

    def implementsOnly(*interfaces):
        """Declare that a class implements only the given interfaces.

        Interfaces implemented by base classes are explicitly not inherited.
        """

    def classProvides(*interfaces):
        """Declare that a class (as opposed to instances of the class)
        directly provides the given interfaces.
        """

    def adapts(*classes_or_interfaces):
        """Declare that a class adapts objects of the given classes or
        interfaces."""

    def context(class_or_interface):
        """Declare the context for views, adapters, etc.

        This directive can be used on module and class level.  When
        used on module level, it will set the context for all views,
        adapters, etc. in that module.  When used on class level, it
        will set the context for that particular class."""

    def name(name):
        """Declare the name of a view or adapter/multi-adapter.

        This directive can only be used on class level."""

    def title(title):
        """Set a human-readable title for a component (e.g. a
        permission, menu item, etc.).

        This directive expects pure ASCII strings or Unicode and can
        only be used on a class level."""

    def description(description):
        """Set a human-readable description for a component (e.g. a
        permission, menu item, etc.).

        This directive expects pure ASCII strings or Unicode and can
        only be used on a class level."""

    def provides(interface):
        """Explicitly specify with which interface a component will be
        looked up."""

    def global_utility(factory, provides=None, name=u''):
        """Register a global utility.

        factory - the factory that creates the global utility
        provides - the interface the utility should be looked up with
        name - the name of the utility
        """

    def global_adapter(factory, adapts=None, provides=None, name=u''):
        """Register a global adapter.

        factory - the adapter factory, a callable
        adapts - an interface or list of interfaces adapted
        provides - the interface provided by the adapter
        name - the name of the adapter
        """

    def direct():
        """Specify whether the class should be used for the component
        or whether it should be used to instantiate the component.

        This directive can be used on GlobalUtility-based classes to
        indicate whether the class itself should be registered as a
        utility, or an instance of it.
        """

    def order(value=None):
        """Control the ordering of components.

        If the value is specified, the order will be determined by sorting on
        it.
        If no value is specified, the order will be determined by definition
        order within the module.
        If the directive is absent, the order will be determined by class name.
        (unfortunately our preferred default behavior on absence which would
        be like grok.order() without argument is hard to implement in Python)

        Inter-module order is by dotted name of the module the
        components are in; unless an explicit argument is specified to
        ``grok.order()``, components are grouped by module.

        The function grok.util.sort_components can be used to sort
        components according to these rules.
        """


class IDecorators(Interface):

    def subscribe(*classes_or_interfaces):
        """Declare that a function subscribes to an event or a
        combination of objects and events."""

    def adapter(*classes_or_interfaces):
        """Describes that a function adapts an object or a combination
        of objects.
        """

    def implementer(*interfaces):
        """Describes that a function that's used as an adapter
        implements an interface or a number of interfaces.
        """

    def provider(*interfaces):
        """Describes that a function directly provides an interface or a
        number of interfaces.
        """


class IGrokErrors(Interface):

    def GrokError(message, component):
        """Error indicating that a problem occurrend during the
        grokking of a module (at "grok time")."""

    def GrokImportError(*args):
        """Error indicating a problem at import time."""


class IMartianAPI(Interface):
    """Part of Martian's API exposed by grokcore.component.
    """

    ClassGrokker = Attribute("Grokker for classes.")

    GlobalGrokker = Attribute("Grokker that's invoked for a module.")

    InstanceGrokker = Attribute("Grokker for instances.")


class IGrokcoreComponentAPI(
    IBaseClasses,
    IDecorators,
    IDirectives,
    IGrokErrors,
    IMartianAPI,
    ):
    """grokcore.component's public API.
    """

    getSiteManager = Attribute('Get the site manager for the nearest site.')

    provideAdapter = Attribute('Registers an adapters')

    provideHandler = Attribute('Registers an handler')

    provideInterface = Attribute('Regsiters an interfaces as a utility')

    provideSubscriptionAdapter = Attribute(
        'Registers an subscriptions adapter')

    provideUtility = Attribute('Registers an utility')

    querySubscriptions = Attribute("Function to query subscriptions.")

    queryOrderedSubscriptions = Attribute(
        "Function to query subscription in order.")

    queryMultiSubscriptions = Attribute("Function to query subscriptions.")

    queryOrderedMultiSubscriptions = Attribute(
        "Function to query subscriptions in order.")

    sort_components = Attribute(
        'Sort a list of components using the information provided by '
        '`grok.order`.')
