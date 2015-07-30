"""
This file is used by viewlet_context. It defines a model that the viewlets
and viewlet manager should *not* be associating with.
"""

import grokcore.view as grok

class Club(grok.Context):
    pass

