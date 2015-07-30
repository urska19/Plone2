"""
A permission has to be defined first (using grok.Permission for example)
before it can be used in grok.require().

  >>> grok.testing.grok(__name__)

  >>> from zope.security.checker import ProxyFactory, getChecker
  >>> obj = ProtectedObject()
  >>> obj = ProxyFactory(obj)
  >>> checker = getChecker(obj)
  >>> checker.permission_id('protected')
  'zope.View'
"""
import grokcore.security as grok

class ProtectedObject(grok.Context):
    protected = 'this is protected'
