"""
Views either need an associated template or a ``render`` method:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  ConfigurationExecutionError: martian.error.GrokError: View <class 'grokcore.view.tests.view.notemplateorrender.CavePainting'>
  has no associated template or 'render' method.
  in:

"""

import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class CavePainting(grok.View):
    pass
