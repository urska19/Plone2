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
from zope import interface
from zope.viewlet.interfaces import IViewletManager as IViewletManagerBase

import grokcore.component.interfaces
import grokcore.security.interfaces
import grokcore.view.interfaces


class IBaseClasses(grokcore.component.interfaces.IBaseClasses,
                   grokcore.security.interfaces.IBaseClasses,
                   grokcore.view.interfaces.IBaseClasses):

    ViewletManager = interface.Attribute("Base class for viewletmanager.")
    Viewlet = interface.Attribute("Base class for viewlet.")


class IDirectives(grokcore.component.interfaces.IDirectives,
                  grokcore.security.interfaces.IDirectives,
                  grokcore.view.interfaces.IDirectives):

    def viewletmanager(manager):
        """Define on which viewlet manager a viewlet is registered.
        """


class IGrokcoreViewletAPI(grokcore.component.interfaces.IGrokcoreComponentAPI,
                          grokcore.security.interfaces.IGrokcoreSecurityAPI,
                          grokcore.view.interfaces.IGrokcoreViewAPI,
                          IBaseClasses, IDirectives):
    pass


class IViewletManager(IViewletManagerBase):
    """The Grok viewlet manager.
    """
