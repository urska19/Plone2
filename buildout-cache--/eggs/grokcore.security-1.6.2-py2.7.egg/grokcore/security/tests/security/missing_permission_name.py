"""
A permission has to have a name (identifier) to be defined.  If it
doesn't, you'll get an error message:

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  GrokError: A permission needs to have a dotted name for its id.
  Use grok.name to specify one.
"""

import grokcore.security as grok

class MissingName(grok.Permission):
    pass
