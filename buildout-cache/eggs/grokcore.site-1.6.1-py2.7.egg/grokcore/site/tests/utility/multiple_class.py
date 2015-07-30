"""
When you try to register multiple classes with the same (interface, name)
combination multiple times using grok.local_utility, we expect an error:

  >>> import grokcore.site.tests.utility.multiple_class_fixture
  Traceback (most recent call last):
    ...
  GrokImportError: ("Conflicting local utility registration
  <class 'grokcore.site.tests.utility.multiple_class_fixture.Fireplace2'>.
  Local utilities are registered multiple times for interface
  <InterfaceClass grokcore.site.tests.utility.multiple_class_fixture.IFireplace>
  and name 'Foo'.",
  <class 'grokcore.site.tests.utility.multiple_class_fixture.Fireplace2'>)
"""
