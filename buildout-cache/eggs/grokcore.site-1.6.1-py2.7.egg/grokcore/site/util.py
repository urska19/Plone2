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

import grokcore.site
from grokcore.site.interfaces import IApplication, ApplicationInitializedEvent
from zope.component.hooks import getSite
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent


def getApplication():
    """Return the nearest enclosing :class:`grokcore.site.Application`.

    Raises :exc:`ValueError` if no application can be found.
    """
    site = getSite()
    if IApplication.providedBy(site):
        return site
    # Another sub-site is within the application. Walk up the object
    # tree until we get to the an application.
    obj = site
    while obj is not None:
        if IApplication.providedBy(obj):
            return obj
        obj = obj.__parent__
    raise ValueError("No application found.")


def create_application(factory, container, name):
    """Creates an application and triggers the events from
    the application lifecycle.
    """
    # Check the factory.
    assert IApplication.implementedBy(factory)

    # Check the availability of the name in the container.
    if name in container:
        raise KeyError(name)

    # Instanciate the application
    application = factory()

    # Trigger the creation event.
    notify(ObjectCreatedEvent(application))

    # Persist the application.
    # This may raise a KeyError.
    container[name] = application

    # Trigger the initialization event.
    notify(ApplicationInitializedEvent(application))

    return application
