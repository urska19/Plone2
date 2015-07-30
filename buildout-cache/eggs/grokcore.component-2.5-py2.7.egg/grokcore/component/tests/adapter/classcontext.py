"""
Explicit class-level context in case of multiple models:

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

"""
import grokcore.component as grok
from zope import interface

class Cave(grok.Context):
    pass

class Club(grok.Context):
    pass

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
    grok.context(Cave)
