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
"""Grokcore.annotation
"""

from grokcore.component import *

from grokcore.annotation.components import Annotation, Model

# BBB These two functions are meant for test fixtures and should be
# imported from grok.testing, not from grok.
from grokcore.annotation.testing import grok

# Our __init__ provides the grok API directly so using 'import grok' is enough.
from grokcore.annotation.interfaces import IGrokcoreAnnotationAPI
from zope.interface import moduleProvides
moduleProvides(IGrokcoreAnnotationAPI)
__all__ = list(IGrokcoreAnnotationAPI)
