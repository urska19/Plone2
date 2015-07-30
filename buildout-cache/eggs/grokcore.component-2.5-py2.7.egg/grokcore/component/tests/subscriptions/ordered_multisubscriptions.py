"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('Tilburg cave')
  >>> martijn = Mammoth('Martijn')

  You can query a subscriptions using multiple components and sort them
  using `grok.order` information:

  >>> ordered_subscriptions = grok.queryOrderedMultiSubscriptions(
  ...     (cave, martijn), IActivity)
  >>> ordered_subscriptions
  [<grokcore.component.tests.subscriptions.ordered_multisubscriptions.Cooking object at ...>,
   <grokcore.component.tests.subscriptions.ordered_multisubscriptions.Gardening object at ...>,
   <grokcore.component.tests.subscriptions.ordered_multisubscriptions.Cleaning object at ...>]

  >>> _ = map(lambda a: a.do(), ordered_subscriptions)
  Martijn is cooking in Tilburg cave!
  Martijn is growing pumpkins in Tilburg cave!
  Martijn is cleaning the Tilburg cave.

  Or choose not to:

  >>> subscriptions = grok.queryMultiSubscriptions(
  ...     (cave, martijn), IActivity)

  (still need to sort them on class name in order to have a working doctest)

  >>> subscriptions = sorted(subscriptions, key=lambda s: s.__class__.__name__)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.ordered_multisubscriptions.Cleaning object at ...>,
   <grokcore.component.tests.subscriptions.ordered_multisubscriptions.Cooking object at ...>,
   <grokcore.component.tests.subscriptions.ordered_multisubscriptions.Gardening object at ...>]

  >>> _ = map(lambda a: a.do(), subscriptions)
  Martijn is cleaning the Tilburg cave.
  Martijn is cooking in Tilburg cave!
  Martijn is growing pumpkins in Tilburg cave!


"""

import grokcore.component as grok
from zope import interface


class Cave(grok.Context):

    def __init__(self, name):
        self.name = name


class Mammoth(grok.Context):

    def __init__(self, name):
        self.name = name


class IActivity(interface.Interface):

    def do():
        """Do something.
        """


class DayTimeActivity(grok.MultiSubscription):
    grok.provides(IActivity)
    grok.adapts(Cave, Mammoth)
    grok.baseclass()

    def __init__(self, where, who):
        self.where = where
        self.who = who

    def do(self):
        print 'Doing nothing.'


class Cleaning(DayTimeActivity):
    grok.order(99)

    def do(self):
        print '%s is cleaning the %s.' % (self.who.name, self.where.name)


class Cooking(DayTimeActivity):
    grok.order(10)

    def do(self):
        print '%s is cooking in %s!' % (self.who.name, self.where.name)


class Gardening(DayTimeActivity):
    grok.order(15)

    def do(self):
        print '%s is growing pumpkins in %s!' % (self.who.name, self.where.name)
