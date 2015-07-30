import grokcore.view as grok
from zope import interface

class IIsAnInterface(interface.Interface):
    grok.skin('skin_name')
