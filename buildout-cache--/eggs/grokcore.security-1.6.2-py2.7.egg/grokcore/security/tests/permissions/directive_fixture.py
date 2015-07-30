import grokcore.component as grok
import grokcore.security

class NotAPermissionSubclass(object):
    grok.name('not really a permission')

class MyRole(object):
    grokcore.security.permissions(NotAPermissionSubclass)
