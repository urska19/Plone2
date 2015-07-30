"""
A permission has to be defined first (using grok.Permission for example)
before it can be used in grok.require().

  >>> grok.testing.grok(__name__)

  >>> from zope.security.checker import ProxyFactory, getChecker
  >>> obj = ProtectedObject()
  >>> obj = ProxyFactory(obj)
  >>> checker = getChecker(obj)
  >>> checker.permission_id('protected')
  'the.permission'
"""
import grokcore.security as grok

class ThePermission(grok.Permission):
    grok.name('the.permission')

class ProtectedObject(grok.Context):
    grok.require(ThePermission)

    protected = 'this is protected'
