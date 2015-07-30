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
"""Grok directives.
"""

import grokcore.component

from grokcore.site.components import LocalUtility

from zope import interface
from zope.interface.interfaces import IInterface

import martian
from martian import util
from martian.error import GrokImportError


class site(martian.Directive):
    """This directive is used to indicate the Grok site
    object for which the component should be used/registered.
    """
    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterfaceOrClass


class local_utility(martian.Directive):
    """The `grokcore.site.local_utility()` directive.

    Place this directive inside of a `grokcore.site.Site` subclass,
    and provide the name of a utility you want activated inside of
    that site::

        class MySite(grokcore.site.Site):
            grok.local_utility(MyMammothUtility)
            ...

    This directive can be supplied several times within the same site.
    Thanks to the presence of this directive, any time an instance of
    your class is created in the Zope database it will have a copy of
    the given local utility installed along with it.

    This directive accepts several normal Component-registration keyword
    arguments, like `provides` and `name`, and uses them each time it
    registers your local utility.

    If you do not supply a `provides` keyword, then Grok attempts to
    guess a sensible default.  Its first choice is to use any
    interface(s) that you listed with the grok.provides() directive
    when defining your utility.  Otherwise, if your utility is a
    subclass of `grokcore.site.LocalUtility`, then Grok will use any
    interfaces that your utility supplies beyond those are supplied
    because of its inheritance from `grokcore.site.LocalUtility`.
    Else, as a final fallback, it checks to see whether the class you
    are registering supplies one, and only one, interface; if so, then
    it can register the utility unambiguously as providing that one
    interface.

    """

    scope = martian.CLASS
    store = martian.DICT

    def factory(self, factory, provides=None, name=u'',
                setup=None, public=False, name_in_container=None):
        if provides is not None and not IInterface.providedBy(provides):
            raise GrokImportError("You can only pass an interface to the "
                                  "provides argument of %s." % self.name)

        if provides is None:
            # We cannot bind the provides directive and get information
            # from the factory, so we do it "manually" as we know how
            # to get to the information.
            dotted = grokcore.component.provides.dotted_name()
            provides = getattr(factory, dotted, None)

        if provides is None:
            if util.check_subclass(factory, LocalUtility):
                baseInterfaces = interface.implementedBy(LocalUtility)
                utilityInterfaces = interface.implementedBy(factory)
                provides = list(utilityInterfaces - baseInterfaces)

                if len(provides) == 0 and len(list(utilityInterfaces)) > 0:
                    raise GrokImportError(
                        "Cannot determine which interface to use "
                        "for utility registration of %r. "
                        "It implements an interface that is a specialization "
                        "of an interface implemented by grok.LocalUtility. "
                        "Specify the interface by either using grok.provides "
                        "on the utility or passing 'provides' to "
                        "grok.local_utility." % factory, factory)
            else:
                provides = list(interface.implementedBy(factory))

            util.check_implements_one_from_list(provides, factory)
            provides = provides[0]

        if (provides, name) in self.frame.f_locals.get(self.dotted_name(), {}):
            raise GrokImportError(
                "Conflicting local utility registration %r. "
                "Local utilities are registered multiple "
                "times for interface %r and name %r." %
                (factory, provides, name), factory)

        info = LocalUtilityInfo(factory, provides, name, setup, public,
                                name_in_container)
        return (provides, name), info


class LocalUtilityInfo(object):
    """The information about how to register a local utility.

    An instance of this class is created for each
    `grokcore.site.local_utility()` in a Grok application's code, to
    remember how the user wants their local utility registered.
    Later, whenever the application creates new instances of the site
    or application for which the local utility directive was supplied,
    this block of information is used as the parameters to the
    creation of the local utility which is created along with the new
    site in the Zope database.

    """
    _order = 0

    def __init__(self, factory, provides, name=u'',
                 setup=None, public=False, name_in_container=None):
        self.factory = factory
        self.provides = provides
        self.name = name
        self.setup = setup
        self.public = public
        self.name_in_container = name_in_container

        self.order = LocalUtilityInfo._order
        LocalUtilityInfo._order += 1

    def __cmp__(self, other):
        # LocalUtilityInfos have an inherit sort order by which the
        # registrations take place.
        return cmp(self.order, other.order)
