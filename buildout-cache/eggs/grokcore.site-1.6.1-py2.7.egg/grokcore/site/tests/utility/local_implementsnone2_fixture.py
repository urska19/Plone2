import grokcore.site
from zope import interface
import persistent

class ISpecialPersistent(persistent.interfaces.IPersistent):
    pass

class Fireplace(grokcore.site.LocalUtility):
    interface.implements(ISpecialPersistent)

class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Fireplace)
