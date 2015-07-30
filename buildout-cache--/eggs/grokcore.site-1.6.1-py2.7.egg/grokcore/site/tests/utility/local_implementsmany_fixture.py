import grokcore.site
from zope import interface

class IHome(interface.Interface):
    pass

class IFireplace(interface.Interface):
    pass

class Fireplace(object):
    interface.implements(IHome, IFireplace)

class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Fireplace)
