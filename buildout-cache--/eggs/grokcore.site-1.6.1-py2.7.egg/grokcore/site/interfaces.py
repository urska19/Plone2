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

from zope.interface import Interface, Attribute, implements
from zope.component.interfaces import IObjectEvent
from grokcore.component.interfaces import IGrokcoreComponentAPI


class IApplication(Interface):
    """Interface to mark the local site used as application root.
    """


class IApplicationInitializedEvent(IObjectEvent):
    """A Grok Application has been created with success and is now ready
    to be used.

    This event can be used to trigger the creation of contents or other tasks
    that require the application to be fully operational : utilities installed
    and indexes created in the catalog."""


class ApplicationInitializedEvent(object):
    """A Grok Application has been created and is now ready to be used.
    """
    implements(IApplicationInitializedEvent)

    def __init__(self, app):
        assert IApplication.providedBy(app)
        self.object = app


class IUtilityInstaller(Interface):
    """This install an utility in a site. Let you have different
    'installation' method if you want (one for Zope2 / Zope3).
    """

    def __call__(site, utility, provides, name=u'',
                 name_in_container=None, public=False, setup=None):
        """Setup an utility.
        """


class IBaseClasses(Interface):
    Site = Attribute("Mixin class for sites.")

    LocalUtility = Attribute("Base class for local utilities.")

    Application = Attribute("Base class for applications.")


class IDirectives(Interface):
    def local_utility(factory, provides=None, name=u'',
                      setup=None, public=False, name_in_container=None):
        """Register a local utility.

        factory - the factory that creates the local utility
        provides - the interface the utility should be looked up with
        name - the name of the utility
        setup - a callable that receives the utility as its single argument,
                it is called after the utility has been created and stored
        public - if False, the utility will be stored below ++etc++site
                 if True, the utility will be stored directly in the site.
                 The site should in this case be a container.
        name_in_container - the name to use for storing the utility
        """

    def provides(interface):
        """Explicitly specify with which interface a component will be
        looked up."""


class IGrokcoreSiteAPI(IGrokcoreComponentAPI, IBaseClasses, IDirectives):
    """grokcore.site's public API."""

    IApplication = Attribute('The application model interface')

    IApplicationInitializedEvent = Attribute(
        'The application initialized event interface')

    ApplicationInitializedEvent = Attribute(
        'The application initialized event factory')

    def getSite():
        """Get the current site."""

    def getApplication():
        """Return the nearest enclosing `grok.Application`."""
