"""
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.subscriptions.multisubscriptions_no_adapts.CaveGardenRenovator'>
  must specify which contexts it adapts (use the 'adapts' directive to specify).

"""

import grokcore.component as grok
from zope import interface

class IRenovate(interface.Interface):

    def takedown():
        pass

class CaveGardenRenovator(grok.MultiSubscription):
    grok.provides(IRenovate)
