"""
You can't call grok.context multiple times on module level:

  >>> import grokcore.component.tests.adapter.modulecontextmultiple_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be called once per
  class or module.

"""
