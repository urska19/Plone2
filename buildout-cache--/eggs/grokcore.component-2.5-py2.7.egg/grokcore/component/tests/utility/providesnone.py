"""
Subclasses of grok.GlobalUtility must implement exactly one interface:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: <class 'grokcore.component.tests.utility.providesnone.Club'>
  must provide at least one interface (use zope.interface.classProvides
  to specify).
"""
import grokcore.component as grok

class Club(grok.GlobalUtility):
    grok.direct()
