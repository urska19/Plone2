"""
Prove that we can instantiate things from unit tests without grokking.

  >>> view = Ungrokked(None, None)
  
This should not raise an exception, at least.

  >>> view.static is None
  True
  >>> view.__name__ is None
  True
  
"""
import grokcore.view as grok

class Ungrokked(grok.View):
    pass