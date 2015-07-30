import grokcore.component as grok
from zope import interface

class Cave(grok.Context):
    pass

class Club(grok.Context):
    pass

grok.context(Cave)
grok.context(Club)
