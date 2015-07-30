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

from zope.interface import implements

from grokcore.component.interfaces import IContext


class Adapter(object):
    """Base class for an adapter that adapts a single object (commonly referred
    to as the *context*).

    Use the ``context`` directive to specify which object to adapt and the
    ``implements`` directive to specify which interface the adapter will
    provide. If it's a named adapter, you may use the ``name`` directive to
    specify the name.

    .. attribute:: context

       The adapted object.

    """

    def __init__(self, context):
        self.context = context


class MultiAdapter(object):
    """Base class for an adapter that adapts *n* objects (where *n>=1*).

    Use the ``adapts`` directive to specify which kinds of objects are adapted
    and the ``implements`` directive to specify which interface the adapter
    will provide. If it's a named multi-adapter, you may use the ``name``
    directive to specify the name.

    Note that contrary to the Adapter, the MultiAdapter base class does not
    provide an `__init__` method. An `__init__` needs to accept the same number
    of arguments as are used in the `adapts` directive.

    """
    pass


class GlobalUtility(object):
    """Base class to define a globally registered utility.

    Base class for a globally registered utility. Unless you use the ``direct``
    directive to indicate that the class itself should be registered as a
    utility, the class will automatically be instantiated, therefore the
    constructor may not take any arguments. Use the ``implements`` directive to
    specify which interface the utility provides, or if that is not
    unambiguous, also use the ``provides`` directive to specify which of the
    implemented interfaces should be used when registering the utility. If it's
    a named utility, you may use the ``name`` directive to specify the name.

    """
    pass


class Subscription(object):
    """Base class for a subscription adapter.

    Subscriptions are similar to adapters, except that it is possible to
    register multiple unnamed subscriptions for identical ``context`` and
    ``provides``.

    Use the ``context`` directive to explicitly set the interface to adapt
    from. When omitted the current context is assumed. Use the ``implements``
    directive to specify which interface the subscription provides, or if that
    is not unambiguous, also use the ``provides`` directive to specify which of
    the implemented interfaces should be used when registering the subscription.

    """

    def __init__(self, context):
        self.context = context


class MultiSubscription(object):
    """Base class for a subscription multi-adapter.

    MultiSubscriptions are similar to multi adapters, except that it is
    possible to register multiple unnamed subscriptions for identical
    ``adapts`` and ``provides``.

    Use the ``adapts`` directive to explicitly set the multiple interfaces to
    adapt from. Use the ``implements`` directive to specify which interface the
    subscription provides, or if that is not unambiguous, also use the
    ``provides`` directive to specify which of the implemented interfaces
    should be used when registering the multi subscription.

    """


class Context(object):
    """Subclasses of this will automatically be found as potential contexts for
    adapters and other types of context-dependent components.

    """
    implements(IContext)
