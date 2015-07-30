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
"""Grok utility functions.
"""
from martian.error import GrokError
from zope.component import queryUtility
from zope.security.interfaces import IPermission
from zope.security.protectclass import protectName
from zope.security.protectclass import protectSetAttribute

def protect_getattr(class_, name, permission=None):
    """Install a getattr permission check for the attribute ``name``.

    If ``permission`` is not supplied, access will be public.
    """
    permission = check_or_default_permission(class_, permission)
    protectName(class_, name, permission)

def protect_setattr(class_, name, permission=None):
    """Install a setattr permission check for the attribute ``name``.

    If ``permission`` is not supplied, access will be public.
    """
    permission = check_or_default_permission(class_, permission)
    protectSetAttribute(class_, name, permission)

def check_or_default_permission(class_, permission):
    """Return default permission (zope.View) if permission is None,
    otherwise make sure permission has been defined.
    """
    if permission is None:
        permission = 'zope.View'
    else:
        check_permission(class_, permission)
    return permission

def check_permission(factory, permission):
    """Check whether a permission is defined.

    If not, raise error for factory.
    """
    if queryUtility(IPermission, name=permission) is None:
       raise GrokError('Undefined permission %r in %r. Use '
                       'grok.Permission first.'
                       % (permission, factory), factory)
