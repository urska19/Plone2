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
"""Grok interfaces
"""
from zope.interface import Interface, Attribute
from zope.dottedname.resolve import resolve

def api(name):
    try:
        return True, resolve(name)
    except ImportError:
        return False, Interface


HAVE_ROLE, IRole = api('zope.securitypolicy.interfaces.IRole')


class IBaseClasses(Interface):
    Permission = Attribute("Base class for permissions.")

    if HAVE_ROLE:
        Role = Attribute("Base class for roles.")


class IDirectives(Interface):

    def require(permission):
        """Protect a view class or an XMLRPC method with ``permission``.

        ``permission`` must already be defined, e.g. using
        grok.Permission.

        grok.require can be used as a class-level directive or as a
        method decorator."""

    def permissions(permissions):
        """Specify the permissions that comprise a role.
        """


class IGrokcoreSecurityAPI(IBaseClasses, IDirectives):
    Public = Attribute("Permission identifier to denote public access.")
