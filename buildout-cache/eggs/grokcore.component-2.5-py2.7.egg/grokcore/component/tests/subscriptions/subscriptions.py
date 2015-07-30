"""
  >>> grok.testing.grok(__name__)

  >>> cave = Cave('sweet home')

  >>> subscriptions = grok.querySubscriptions(cave, ICleaner)
  >>> subscriptions
  [<grokcore.component.tests.subscriptions.subscriptions.MondayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.subscriptions.SaturdayCleaner object at ...>,
   <grokcore.component.tests.subscriptions.subscriptions.WednesdayCleaner object at ...>]

  >>> _ = map(lambda s: s.work(), subscriptions)
  Monday cleaning sweet home!
  Saturday cleaning sweet home!
  Wednesday cleaning sweet home!

  Subscription adapters are not registered as regular adapters:

  >>> component.queryAdapter(cave, ICleaner)

"""

import grokcore.component as grok
from zope import interface, component


class Cave(grok.Context):

    def __init__(self, name):
        self.name = name


class ICleaner(interface.Interface):

    def work():
        """Clean that cave.
        """

class MondayCleaner(grok.Subscription):
    grok.implements(ICleaner)

    def work(self):
        print 'Monday cleaning %s!' % self.context.name


class WednesdayCleaner(grok.Subscription):
    grok.provides(ICleaner)

    def work(self):
        print 'Wednesday cleaning %s!' % self.context.name


class SaturdayCleaner(grok.Subscription):
    grok.implements(ICleaner)

    def work(self):
        print 'Saturday cleaning %s!' % self.context.name

