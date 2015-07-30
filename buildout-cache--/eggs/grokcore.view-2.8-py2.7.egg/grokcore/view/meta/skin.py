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
"""Grokkers for the skin support."""


from zope.interface.interface import InterfaceClass
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IBrowserSkinType

import martian
from martian.error import GrokError

import grokcore.view
import grokcore.component

_skin_not_used = object()


class SkinInterfaceDirectiveGrokker(martian.InstanceGrokker):
    martian.component(InterfaceClass)

    def grok(self, name, interface, module_info, config, **kw):
        skin = grokcore.view.skin.bind(default=_skin_not_used).get(interface)
        if skin is _skin_not_used:
            # The skin directive is not actually used on the found interface.
            return False

        if not interface.extends(IBrowserRequest):
            # For layers it is required to extend IBrowserRequest.
            raise GrokError(
                "The grok.skin() directive is used on interface %r. "
                "However, %r does not extend IBrowserRequest which is "
                "required for interfaces that are used as layers and are to "
                "be registered as a skin."
                % (interface.__identifier__, interface.__identifier__),
                interface,
                )
        config.action(
            discriminator=('utility', IBrowserSkinType, skin),
            callable=grokcore.component.provideInterface,
            args=(skin, interface, IBrowserSkinType))
        return True
