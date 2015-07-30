"""
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: No module-level context for
  <class 'grokcore.component.tests.subscriptions.subscriptions_no_context.CaveProcessor'>,
  please use the 'context' directive.

"""

import grokcore.component as grok
from zope import interface

class ITask(interface.Interface):

    def finish():
        pass

class CaveProcessor(grok.Subscription):
    grok.provides(ITask)
