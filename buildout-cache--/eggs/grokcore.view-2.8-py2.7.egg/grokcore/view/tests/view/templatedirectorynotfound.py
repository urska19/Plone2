"""
If the template directory you specify doesn't exist, you have a comprehensible
error:

  >>> grok.testing.grok(
  ...     'grokcore.view.tests.view.templatedirectorynotfound_fixture')
  Traceback (most recent call last):
  ...
  GrokImportError: The directory 'idontexit' specified by the
  'templatedir' directive cannot be found.

"""

from grokcore import view as grok
