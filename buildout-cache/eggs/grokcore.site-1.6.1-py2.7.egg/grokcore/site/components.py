##############################################################################
#
# Copyright (c) 2006-2009 Zope Foundation and Contributors.
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

from persistent import Persistent
from grokcore.component.interfaces import IContext
from grokcore.site.interfaces import IApplication
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container.contained import Contained
from zope.interface import implements
from zope.site.site import SiteManagerContainer


class BaseSite(object):
    """Mixin to grok sites in Grok applications.

    It's used to let different implementation of sites to exists, and
    still being grokked correctly.
    """


class Site(BaseSite, SiteManagerContainer):
    """Mixin for creating sites in Grok applications.

    When an application :class:`grok.Model` or :class:`grok.Container`
    also inherits from :class:`grokcore.site.Site`, then it can
    additionally support the registration of local Component
    Architecture entities like :class:`grokcore.site.LocalUtility` and
    :class:`grok.Indexes` objects; see those classes for more
    information.
    """


class Application(Site):
    """Mixin for creating Grok application objects.

    When a :class:`grokcore.content.Container` (or a
    :class:`grokcore.content.Model`, though most developers
    use containers) also inherits from :class:`grokcore.site.Application`,
    it not only gains the component registration abilities of a
    :class:`grokcore.site.site`, but will also be listed in the
    Grok admin control panel as one of the applications
    that the admin can install directly at the root of their Zope
    database.
    """
    implements(IApplication)


class LocalUtility(Contained, Persistent):
    """The base class for local utilities in Grok applications.

    Defines a utility that will be registered local to a :class:`Site`
    or :class:`grok.Application`.
    
    Although application developers can create local utilies without
    actually subclassing :class:`LocalUtility`, they gain three
    benefits from doing so.  First, their code is more readable
    because their classes "look like" local utilities to casual
    readers.  Second, their utility will know how to persist itself to
    the Zope database, which means that they can set its object
    attributes and know that the values are getting automatically
    saved.  Third, they can omit the `grok.provides()` directive
    naming the interface that the utility provides, if their class
    only `grok.implements()` a single interface (unless the interface
    is one that the `grok.LocalUtility` already implements, in which
    case Grok cannot tell them apart, and `grok.provides()` must be
    used explicitly anyway).
    """
    implements(IContext, IAttributeAnnotatable)
