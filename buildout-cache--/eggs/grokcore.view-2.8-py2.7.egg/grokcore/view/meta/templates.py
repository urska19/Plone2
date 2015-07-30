#############################################################################
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
"""Grokkers for templates."""
import sys
import martian

from grokcore.view import components
from grokcore.view import templatereg

class ModulePageTemplateGrokker(martian.InstanceGrokker):
    martian.component(components.BaseTemplate)
    # this needs to happen before any other grokkers execute that actually
    # use the templates
    martian.priority(1000)

    def grok(self, name, instance, module_info, config, **kw):
        # We set the configuration action order to 0, to be sure to
        # register templates first.
        config.action(
            discriminator=None,
            callable=templatereg.register_inline_template,
            args=(module_info, name, instance),
            order=0)
        config.action(
            discriminator=None,
            callable=instance._annotateGrokInfo,
            args=(name, module_info.dotted_name))
        return True


class FilesystemPageTemplateGrokker(martian.GlobalGrokker):
    # Do this early on, but after ModulePageTemplateGrokker, as
    # findFilesystem depends on module-level templates to be already
    # grokked for error reporting.
    martian.priority(999)

    def grok(self, name, module, module_info, config, **kw):
        # We set the configuration action order to 0, to be sure to
        # register templates first.
        config.action(
            discriminator=None,
            callable=templatereg.register_directory,
            args=(module_info,),
            order=0)
        return True


class UnassociatedTemplatesGrokker(martian.GlobalGrokker):
    martian.priority(-1001)
    # XXX: The action should be registered only once, not for each module.
    # There should be a way to register the action without a module grokker...
    _action_registered = False

    def grok(self, name, module, module_info, config, **kw):
        if not self._action_registered:
            self._action_registered = True
            # We set the configuration action order to very very high
            # to be sure to check unused template at the end only.
            config.action(
                discriminator=None,
                callable=templatereg.check_unassociated,
                args=(),
                order=sys.maxint
                )
        return True

