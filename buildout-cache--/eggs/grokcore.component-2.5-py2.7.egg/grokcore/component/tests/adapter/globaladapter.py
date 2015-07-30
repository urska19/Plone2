"""
  >>> grok.testing.grok(__name__)
  >>> from zope.component import getAdapter, getMultiAdapter

  >>> cave = Cave()
  >>> fireplace = Fireplace()

  >>> home = IHome(cave)
  >>> home.id
  u'one'

  >>> home = getAdapter(cave, IHome, name=u"two")
  >>> home.id
  u'two'

  >>> home = getAdapter(cave, IHome, name=u"three")
  >>> home.id
  u'three'

  >>> home = getAdapter(cave, IHome, name=u"four")
  >>> home.id
  u'four'

  >>> home = getAdapter(fireplace, IHome, name=u"five")
  >>> home.id
  u'five'

  >>> home = getMultiAdapter((cave, fireplace), IHome)
  >>> home.id
  u'six'

  >>> home = getAdapter(fireplace, IHome, name=u'seven')
  >>> home.id
  u'seven-a'

  >>> home = getMultiAdapter((cave, fireplace), IHome, name=u'seven')
  >>> home.id
  u'seven-b'

  >>> garage = getAdapter(cave, IGarage, name='named_garage_factory_name')
  >>> garage.id
  u"I'm a garage"

  >>> garage = getAdapter(cave, IGarage)
  >>> garage.id
  u"I'm a garage"

"""

import grokcore.component as grok
from zope import interface
from zope.interface import implementer


class Cave(grok.Context):
    pass


class Fireplace(object):
    pass


class IHome(interface.Interface):
    pass


class Home(object):
    grok.implements(IHome)

    def __init__(self, id):
        self.id = id


class CaveHomeFactory(object):
    grok.implements(IHome)

    def __init__(self, id):
        self.id = id

    def __call__(self, context):
        return Home(self.id)


class CaveFireplaceHomeFactory(object):

    def __init__(self, id):
        self.id = id

    def __call__(self, cave, fireplace):
        return Home(self.id)


factory1 = CaveHomeFactory(u"one")
factory2 = CaveHomeFactory(u"two")
factory3 = CaveHomeFactory(u"three")
factory4 = CaveHomeFactory(u"four")
factory5 = CaveHomeFactory(u"five")
factory6 = CaveFireplaceHomeFactory(u"six")
factory7a = CaveHomeFactory(u"seven-a")
factory7b = CaveFireplaceHomeFactory(u"seven-b")

# make some direct assertions

implementer(IHome)(factory3)
implementer(IHome)(factory4)
implementer(IHome)(factory5)
implementer(IHome)(factory6)
implementer(IHome)(factory7a)
implementer(IHome)(factory7b)

grok.adapter(Fireplace)(factory5)
grok.adapter(Fireplace)(factory7a)
grok.adapter(Cave, Fireplace)(factory7b)

# should accept single value for adapts
grok.global_adapter(factory1, Cave, IHome)
# should accept tuple for adapts
grok.global_adapter(factory2, (Cave,), IHome, name=u"two")
# should look at the provided interface
grok.global_adapter(factory3, Cave, name=u"three")
# should pick the canonical context
grok.global_adapter(factory4, name=u"four")
# should use __component_adapts__
grok.global_adapter(factory5, name=u"five")
# should work as multi-adapter
grok.global_adapter(factory6, (Cave, Fireplace,))
# should use __component_adapts__ adapting one object
grok.global_adapter(factory7a, name=u"seven")
# should use __component_adapts__ adaping two objects
grok.global_adapter(factory7b, name=u"seven")


class IGarage(interface.Interface):
    pass


class NamedGarageFactory(object):
    grok.implements(IGarage)
    grok.name('named_garage_factory_name')

    def __init__(self, context):
        self.id = u"I'm a garage"

implementer(IGarage)(NamedGarageFactory)

# should register a named adapter
grok.global_adapter(NamedGarageFactory, Cave, IGarage)
# should override component's name
grok.global_adapter(NamedGarageFactory, Cave, IGarage, name=u'')
