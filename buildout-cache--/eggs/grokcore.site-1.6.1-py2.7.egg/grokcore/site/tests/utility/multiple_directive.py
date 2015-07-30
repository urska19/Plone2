"""
When you call the grok.local_utility directive multiple times specifying
the same (interface, name) combination, we expect an error:

  >>> import grokcore.site.tests.utility.multiple_directive_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: ("Conflicting local utility registration
  <class 'grokcore.site.tests.utility.multiple_directive_fixture.Fireplace2'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grokcore.site.tests.utility.multiple_directive_fixture.IFireplace>
  and name u''.",
  <class 'grokcore.site.tests.utility.multiple_directive_fixture.Fireplace2'>)
"""
