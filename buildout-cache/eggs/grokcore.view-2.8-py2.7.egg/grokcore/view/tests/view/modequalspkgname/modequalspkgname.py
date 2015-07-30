"""
The sense of this module is, to have the same name as the package it
resides in. Grokking it should not provoke an `unassociated template`
error or warning.
"""
import grokcore.view as grok
class Cave(grok.Context):
    pass

class Index(grok.View):
    pass # see modequalspkgname_templates
