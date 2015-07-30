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

from grokcore.security.components import Permission
from grokcore.security.components import Public
from grokcore.security.directive import require, permissions

# Import this module so that it's available as soon as you import the
# 'grokcore.security' package.  Useful for tests and interpreter examples.
import grokcore.security.testing

# Only export public API
from grokcore.security.interfaces import IGrokcoreSecurityAPI, HAVE_ROLE
if HAVE_ROLE:
    from grokcore.security.components import Role

__all__ = list(IGrokcoreSecurityAPI)
