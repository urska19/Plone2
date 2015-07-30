"""
  >>> grok.testing.grok(__name__)

The permission grokker will register permissions as utilities.  That
means we can look them up again using the Component Architecture:

  >>> from zope.component import getUtility
  >>> from zope.security.interfaces import IPermission
  >>> permission = getUtility(IPermission, 'the.permission')

The permission object we obtain will actually be an instance of the
class we registered:

  >>> isinstance(permission, ThePermission)
  True

The object we obtain also complies with the ``IPermission`` interface,
meaning it has all the required attributes set.

  >>> permission.id
  u'the.permission'
  >>> permission.title
  u'The permission!'
  >>> permission.description
  u'This is *the* permission.'
"""

import grokcore.security as grok

class ThePermission(grok.Permission):
    grok.name('the.permission')
    grok.title('The permission!')
    grok.description('This is *the* permission.')
