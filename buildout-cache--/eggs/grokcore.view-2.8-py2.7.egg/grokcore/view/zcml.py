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
"""Grok ZCML directives."""

from zope.interface import Interface
from zope.schema import TextLine

from grokcore.view.templatereg import file_template_registry


class IIgnoreTemplatesDirective(Interface):
    """Ignore a template pattern.
    """

    pattern = TextLine(
        title=u"Pattern",
        description=u"Pattern of template to ignore.",
        required=True)

def ignoreTemplates(_context, pattern):
    file_template_registry.ignore_templates(pattern)


