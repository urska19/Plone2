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
"""Grokkers for security-related components."""


from grokcore.security.interfaces import HAVE_ROLE

if HAVE_ROLE:
    import martian

    import grokcore.component
    import grokcore.security

    from martian.error import GrokError
    from zope.i18nmessageid import Message
    from zope.securitypolicy.rolepermission import rolePermissionManager
    from zope.securitypolicy.interfaces import IRole

    from grokcore.security.components import Role
    from grokcore.security.directive import permissions
    from grokcore.security.meta.permission import PermissionGrokker
    from grokcore.security.meta.permission import default_fallback_to_name


    class RoleGrokker(martian.ClassGrokker):
        """Grokker for components subclassed from `grok.Role`.

        Each role is registered as a global utility providing the service
        `IRole` under its own particular name, and then granted every
        permission named in its `grok.permission()` directive.

        """
        martian.component(Role)
        martian.priority(martian.priority.bind().get(PermissionGrokker()) - 1)
        martian.directive(grokcore.component.name)
        martian.directive(
            grokcore.component.title, get_default=default_fallback_to_name)
        martian.directive(grokcore.component.description)
        martian.directive(permissions)

        def execute(self, factory, config, name, title, description,
                    permissions, **kw):
            if not name:
                raise GrokError(
                    "A role needs to have a dotted name for its id. Use "
                    "grok.name to specify one.", factory)
            # We can safely convert to unicode, since the directives makes sure
            # it is either unicode already or ASCII.
            if not isinstance(title, Message):
                title = unicode(title)
            if not isinstance(description, Message):
                description = unicode(description)
            role = factory(unicode(name), title, description)

            config.action(
                discriminator=('utility', IRole, name),
                callable=grokcore.component.provideUtility,
                args=(role, IRole, name),
                )

            for permission in permissions:
                config.action(
                    discriminator=('grantPermissionToRole', permission, name),
                    callable=rolePermissionManager.grantPermissionToRole,
                    args=(permission, name),
                    )
            return True
