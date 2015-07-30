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
"""Grok
"""
from grokcore.component import *
from grokcore.security import *
from grokcore.view import *

from grokcore.viewlet.components import Viewlet, ViewletManager
from grokcore.viewlet.directive import viewletmanager

# Import this module so that it's available as soon as you import the
# 'grokcore.view' package.  Useful for tests and interpreter examples.
import grokcore.viewlet.testing

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grokcore.viewlet.interfaces import IGrokcoreViewletAPI
from zope.interface import moduleProvides
moduleProvides(IGrokcoreViewletAPI)
__all__ = list(IGrokcoreViewletAPI)
