import grokcore.site

class Fireplace(object):
    pass

class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Fireplace)
