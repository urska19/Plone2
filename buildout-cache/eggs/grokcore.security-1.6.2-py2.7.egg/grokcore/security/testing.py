##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Grok test helpers
"""
import martian
import grokcore.component
from zope.configuration.config import ConfigurationMachine
from grokcore.component import zcml
from grokcore.security import directive
from grokcore.security import util

class ClasslevelGrokker(martian.ClassGrokker):
    """Simple grokker that looks for grokk.require() directives on a
    class and checks whether the permissione exists."""
    martian.component(grokcore.component.Context)
    martian.directive(directive.require, name='permission')

    def execute(self, factory, config, permission, **kw):
        config.action(
            discriminator=('protectName', factory, 'protected'),
            callable=util.protect_getattr,
            args=(factory, 'protected', permission),
            )
        return True

def grok(module_name):
    config = ConfigurationMachine()
    zcml.do_grok('grokcore.component.meta', config)
    zcml.do_grok('grokcore.security.meta', config)
    zcml.do_grok('grokcore.security.testing', config)
    zcml.do_grok(module_name, config)
    config.execute_actions()
