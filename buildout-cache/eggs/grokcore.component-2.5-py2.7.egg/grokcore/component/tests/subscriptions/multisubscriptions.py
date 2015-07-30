"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('Tilburg cave')
  >>> martijn = Mammoth('Martijn')

  You can query a subscriptions using multiple components. You will get
  all subscriptions registered for office and cave (since office is a
  base class of cave):

  >>> subscriptions = grok.queryMultiSubscriptions((cave, martijn), IActivity)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.multisubscriptions.Sleep object at ...>,
   <grokcore.component.tests.subscriptions.multisubscriptions.Food object at ...>,
   <grokcore.component.tests.subscriptions.multisubscriptions.WritingCode object at ...>]

  >>> _ = map(lambda s: s.do(), subscriptions)
  Martijn is sleeping at Tilburg cave.
  Martijn is feeding himself at Tilburg cave.
  Martijn is writing code at Tilburg cave!


  Now, Martijn goes to the office. You will only get subscriptions
  registered for office:

  >>> office = Office('Grok corp(r)(tm) headquarters')
  >>> office_subscriptions = grok.queryMultiSubscriptions(
  ...     (office, martijn), IActivity)
  >>> office_subscriptions
  [<grokcore.component.tests.subscriptions.multisubscriptions.Sleep object at ...>]

  >>> _ = map(lambda s: s.do(), office_subscriptions)
  Martijn is sleeping at Grok corp(r)(tm) headquarters.

"""

import grokcore.component as grok
from zope import interface


class Office(grok.Context):

    def __init__(self, name):
        self.name = name


# All caves are a kind of office.
class Cave(Office):
    pass


class Mammoth(grok.Context):

    def __init__(self, name):
        self.name = name


class IActivity(interface.Interface):

    def do():
        """Do something.
        """

class Sleep(grok.MultiSubscription):
    grok.implements(IActivity)
    grok.adapts(Office, Mammoth)

    def __init__(self, where, who):
        self.where = where
        self.who = who

    def do(self):
        print '%s is sleeping at %s.' % (self.who.name, self.where.name)


class DayTimeActivity(grok.MultiSubscription):
    grok.implements(IActivity)
    grok.adapts(Cave, Mammoth)
    grok.baseclass()

    def __init__(self, where, who):
        self.where = where
        self.who = who

    def do(self):
        print 'nothing'


class Food(DayTimeActivity):

    def do(self):
        print '%s is feeding himself at %s.' % (self.who.name, self.where.name)


class WritingCode(DayTimeActivity):

    def do(self):
        print '%s is writing code at %s!' % (self.who.name, self.where.name)
