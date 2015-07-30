"""
A Role component optionally defines what permission it comprises.

The grok.permissions() directive is used to specify the set of permissions
that are aggregated in the particular Role. The permissions can be referenced
by "name" or by class.

  >>> grokcore.security.testing.grok(__name__)
"""

import grokcore.component as grok
import grokcore.security.testing
from grokcore.security import Role
from grokcore.security import Permission, permissions
import zope.interface

class FirstPermission(Permission):
    grok.name('first permission')

class SecondPermission(Permission):
    grok.name('second permission')

class RoleComprisingTwoPermissionsByName(Role):
    grok.name('ByName')
    permissions(
        'first permission',
        'second permission'
        )

class RoleComprisingTwoPermissionsByClass(Role):
    grok.name('ByClass')
    permissions(
        FirstPermission,
        SecondPermission
        )
