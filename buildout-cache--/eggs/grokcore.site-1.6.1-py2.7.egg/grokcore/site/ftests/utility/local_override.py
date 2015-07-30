"""
Local Utilities can be registered on subclasses of grok.Site using
grok.local_utility:

  >>> cave = SpikyCave()
  >>> getRootFolder()['cave'] = cave

  >>> from zope import component
  >>> from zope.site.hooks import getSite, setSite
  >>> setSite(cave)

  >>> club = component.getUtility(IClub)
  >>> IClub.providedBy(club)
  True
  >>> isinstance(club, SpikyClub)
  True

  >>> list(cave.getSiteManager().keys())
  [u'SpikyClub']
"""
import grokcore.site
from zope import interface

class IClub(interface.Interface):
    pass

class Club(grokcore.site.LocalUtility):
    interface.implements(IClub)

class SpikyClub(grokcore.site.LocalUtility):
    interface.implements(IClub)

class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Club)

class SpikyCave(Cave):
    grokcore.site.local_utility(SpikyClub)

