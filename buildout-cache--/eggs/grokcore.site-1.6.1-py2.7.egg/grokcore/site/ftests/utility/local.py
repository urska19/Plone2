"""
Local Utilities can be registered on subclasses of grok.Site using
grok.local_utility:

  >>> cave = Cave()
  >>> getRootFolder()["cave"] = cave

  >>> from zope import component
  >>> from zope.site.hooks import getSite, setSite
  >>> setSite(cave)

  >>> fireplace = component.getUtility(IFireplace)
  >>> IFireplace.providedBy(fireplace)
  True
  >>> isinstance(fireplace, Fireplace)
  True

  >>> club = component.getUtility(IClub)
  >>> IClub.providedBy(club)
  True
  >>> isinstance(club, Club)
  True

  >>> spiky = component.getUtility(IClub, name='spiky')
  >>> IClub.providedBy(spiky)
  True
  >>> isinstance(spiky, SpikyClub)
  True

  >>> mammoth = component.getUtility(IMammoth)
  >>> IMammoth.providedBy(mammoth)
  True
  >>> isinstance(mammoth, Mammoth)
  True

  >>> tiger = component.getUtility(IMammoth, name='tiger')
  >>> IMammoth.providedBy(tiger)
  True
  >>> isinstance(tiger, SabretoothTiger)
  True

  >>> painting = component.getUtility(IPainting, name='blackandwhite')
  >>> IPainting.providedBy(painting)
  True
  >>> isinstance(painting, CavePainting)
  True

  >>> colored = component.getUtility(IPainting, name='color')
  >>> IPainting.providedBy(colored)
  True
  >>> isinstance(colored, ColoredCavePainting)
  True

Since it is a local utility, it is not available outside its site:

  >>> setSite(None)
  >>> component.getUtility(IFireplace)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IFireplace>, '')

  >>> component.getUtility(IClub)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IClub>, '')

  >>> component.getUtility(IClub, name='spiky')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IClub>, 'spiky')

  >>> component.getUtility(IMammoth)
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IMammoth>, '')

  >>> component.getUtility(IMammoth, name='tiger')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IMammoth>, 'tiger')

  >>> component.getUtility(IPainting, name='blackandwhite')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IPainting>, 'blackandwhite')

  >>> component.getUtility(IPainting, name='color')
  Traceback (most recent call last):
    ...
  ComponentLookupError: (<InterfaceClass grokcore.site.ftests.utility.local.IPainting>, 'color')
"""
import grokcore.site
from zope import interface
import persistent

class IFireplace(interface.Interface):
    pass

class IClub(interface.Interface):
    pass

class ISpiky(interface.Interface):
    pass

class IMammoth(interface.Interface):
    pass

class Fireplace(grokcore.site.LocalUtility):
    interface.implements(IFireplace)

class Club(object):
    interface.implements(IClub)

class SpikyClub(object):
    interface.implements(IClub, ISpiky)

class Mammoth(grokcore.site.LocalUtility):
    interface.implements(IMammoth, IClub)

class SabretoothTiger(grokcore.site.LocalUtility):
    interface.implements(IMammoth, IClub)
    grokcore.site.provides(IMammoth)

class IPainting(persistent.interfaces.IPersistent):
    pass

class CavePainting(grokcore.site.LocalUtility):
    interface.implements(IPainting)

class ColoredCavePainting(grokcore.site.LocalUtility):
    interface.implements(IPainting)
    grokcore.site.provides(IPainting)

class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Fireplace)
    grokcore.site.local_utility(Club)
    grokcore.site.local_utility(SpikyClub, provides=IClub, name='spiky')
    grokcore.site.local_utility(Mammoth, provides=IMammoth)
    grokcore.site.local_utility(SabretoothTiger, name='tiger')
    grokcore.site.local_utility(CavePainting, name='blackandwhite', provides=IPainting)
    grokcore.site.local_utility(ColoredCavePainting, name='color')
