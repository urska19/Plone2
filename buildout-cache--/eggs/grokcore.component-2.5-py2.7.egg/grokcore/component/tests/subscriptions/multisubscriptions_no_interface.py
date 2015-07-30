"""
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.subscriptions.multisubscriptions_no_interface.CaveGardenRedecorator'>
  must implement at least one interface (use grok.implements to specify).

"""

import grokcore.component as grok


class Cave(grok.Context):
    pass

class Garden(grok.Context):
    pass

class CaveGardenRedecorator(grok.MultiSubscription):
    pass
