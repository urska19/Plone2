"""
You can also specify interfaces instead of classes with
`grok.context` (class-level):

  >>> grok.testing.grok(__name__)

  >>> cave = Cave()
  >>> home = IHome(cave)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

  >>> hole = Hole()
  >>> home = IHome(hole)

  >>> IHome.providedBy(home)
  True
  >>> isinstance(home, Home)
  True

"""
import grokcore.component as grok
from zope import interface

class ICave(interface.Interface):
    pass

class Cave(grok.Context):
    grok.implements(ICave)

class Hole(grok.Context):
    grok.implements(ICave)

class IHome(interface.Interface):
    pass

class Home(grok.Adapter):
    grok.implements(IHome)
    grok.context(ICave)
