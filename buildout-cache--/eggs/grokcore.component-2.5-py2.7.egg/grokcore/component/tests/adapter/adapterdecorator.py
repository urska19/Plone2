"""
  >>> grok.testing.grok(__name__)
  >>>
  >>> cave = Cave()
  >>> home = IHome(cave)
  >>> home.id
  u'default'
  >>> IHome.providedBy(home)
  True
  >>>
  >>> isinstance(home, Home)
  True
  >>> morehome = IMoreHome(cave)
  >>> morehome.id
  u'default'
  >>> IHome.providedBy(morehome)
  True
  >>> isinstance(morehome, Home)
  True
  >>> yetanotherhome = IYetAnotherHome(cave)
  >>> IHome.providedBy(yetanotherhome)
  True
  >>> isinstance(yetanotherhome, Home)
  True
  >>> yetanotherhome.id
  u'default'

  >>> from grokcore.component.tests.adapter import noarguments_fixture
  Traceback (most recent call last):
  ...
  GrokImportError: @grok.adapter requires at least one argument.

  >>> from grokcore.component.tests.adapter import functionasargument_fixture
  Traceback (most recent call last):
  ...
  GrokImportError: @grok.adapter requires at least one argument.

  >>> from zope.component import getAdapter
  >>> home = getAdapter(cave, IHome, name='home')
  >>> home.id
  u'secondary'

"""

import grokcore.component as grok
from zope import interface

class IDummy(interface.Interface):
    pass

class ICave(interface.Interface):
    pass

class IHome(interface.Interface):
    pass

class IMoreHome(interface.Interface):
    pass

class IYetAnotherHome(interface.Interface):
    pass

class Cave(grok.Context):
    grok.implements(ICave)
    pass

class Home(object):
    grok.implements(IHome)
    
    def __init__(self, id=u"default"):
        self.id = id

@grok.adapter(Cave)
@grok.implementer(IHome)
def home_for_cave(cave):
    return Home()

@grok.adapter(ICave)
@grok.implementer(IMoreHome)
def more_home_for_cave(cave):
    return Home()

@grok.implementer(IYetAnotherHome)
def yet_another_home_for_cave(cave):
    return Home()

@grok.adapter(Cave, name=u"home")
@grok.implementer(IHome)
def home_for_cave_named(cave):
    return Home(u"secondary")