"""
We expect the module-level grok.context to be inherited by subclasses of
an adapter that is associated with this directive. FooAdapter is such
an adapter, defined in inherit_fixture. In this module we've inherited
from it.

Explicit module-level context for an imported model:

  >>> grok.testing.grok(__name__)

  >>> from zope import component
  >>> o = component.getAdapter(inherit_fixture.Foo(), inherit_fixture.IAnder,
  ...   name='bar')
  >>> isinstance(o, BarAdapter)
  True
"""
import grokcore.component as grok
from grokcore.component.tests.inherit import inherit_fixture

# FooAdapter has a module-level grok.context to associate it
class BarAdapter(inherit_fixture.FooAdapter):
    grok.name('bar')
