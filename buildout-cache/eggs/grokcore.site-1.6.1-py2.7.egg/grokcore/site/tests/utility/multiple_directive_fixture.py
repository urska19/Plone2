import grokcore.site
from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grokcore.site.LocalUtility):
    interface.implements(IFireplace)

class Fireplace2(grokcore.site.LocalUtility):
    interface.implements(IFireplace)
    
class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Fireplace, provides=IFireplace)
    grokcore.site.local_utility(Fireplace2, provides=IFireplace)
