"""
You can't call grok.context multiple times on class level:

  >>> import grokcore.component.tests.adapter.classcontextmultiple_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: The 'context' directive can only be called once per
  class or module.

"""

