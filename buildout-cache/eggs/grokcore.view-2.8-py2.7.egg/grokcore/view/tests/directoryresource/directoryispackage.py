"""
When a directory resource is declared, it is not allowed for it to be a
python package::

  >>> import grokcore.view as grok
  >>> grok.testing.grok(
  ...     'grokcore.view.tests.directoryresource.directoryispackage_fixture')
  Traceback (most recent call last):
    ...
  GrokError: The 'foo' resource directory must not be a python package.
"""
