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
"""Base classes for Grok application components.

"""

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.container import contained
import persistent
import grokcore.component


class Model(grokcore.component.Context):
    """Base class for an object which is able to handle annotations
    """
    grokcore.component.implements(IAttributeAnnotatable)


class Annotation(persistent.Persistent, contained.Contained):
    """The base class for annotation classes in Grok applications.

    Inherits from the :class:`persistent.Persistent` class.
    """
