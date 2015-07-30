"""
  >>> import grokcore.view as grok
  >>> grok.testing.grok(
  ...     'grokcore.view.tests.directoryresource.directoryresources_fixture')

  >>> from zope.interface import Interface
  >>> from zope.component import getAdapter
  >>> from zope.publisher.browser import TestRequest

  >>> resource_foo = getAdapter(TestRequest(), Interface, name='foo')
  >>> resource_foo.context.path.replace('\\\\', '/') # Windows compliance 
  '...grokcore/view/tests/directoryresource/directoryresources_fixture/foo'

  >>> resource_baz = getAdapter(TestRequest(), Interface, name='baz')
  >>> resource_baz.context.path.replace('\\\\', '/') # Windows compliance 
  '...grokcore/view/tests/directoryresource/directoryresources_fixture/bar/baz'

"""
