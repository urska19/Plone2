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
from zope.configuration.fields import GlobalObject
from zope.schema import TextLine

import martian


class IGrokDirective(Interface):
    """Grok a package or module."""

    package = GlobalObject(
        title=u"Package",
        description=u"The package or module to be analyzed by grok.",
        required=False)

    exclude = TextLine(
        title=u"Exclude",
        description=u"Name to exclude in the grokking process.",
        required=False)


# add a cleanup hook so that grok will bootstrap itself again whenever
# the Component Architecture is torn down.
def resetBootstrap():
    # we need to make sure that the grokker registry is clean again
    the_module_grokker.clear()

from zope.testing.cleanup import addCleanUp
addCleanUp(resetBootstrap)

the_multi_grokker = martian.MetaMultiGrokker()
the_module_grokker = martian.ModuleGrokker(the_multi_grokker)


def skip_tests(name):
    return name in ['tests', 'ftests', 'testing']


def grokDirective(_context, package, exclude=None):
    if not exclude:
        exclude = None
    do_grok(package.__name__, _context, extra_exclude=exclude)


def do_grok(dotted_name, config, extra_exclude=None):
    if extra_exclude is not None:

        def exclude_filter(name):
            return skip_tests(name) or extra_exclude == name

    else:
        exclude_filter = skip_tests

    martian.grok_dotted_name(
        dotted_name, the_module_grokker, exclude_filter=exclude_filter,
        config=config)
