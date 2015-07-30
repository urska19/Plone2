"""
By default, a utility is not in the public site; it's in ++etc++site. We can
also specify the utility to be public. It will then be created in the container
that is the site. The name the utility should have in the container can
be controlled using name_in_container:

  >>> cave = Cave()
  >>> getRootFolder()["cave"] = cave

  >>> from zope import component
  >>> from zope.site.hooks import getSite, setSite
  >>> setSite(cave)
  >>> cave['fireplace'] is component.getUtility(IFireplace)
  True

name_in_container can also be used for objects stored under the site manager
(that is in ++etc++site):

   >>> cave2 = Cave2()
   >>> getRootFolder()['cave2'] = cave2
   >>> setSite(cave2)
   >>> (cave2.getSiteManager()['fireplace'] is
   ...  component.getUtility(IFireplace))
   True

"""

import grokcore.site
from zope import interface
from zope.container.btree import BTreeContainer

class IFireplace(interface.Interface):
    pass

class Fireplace(grokcore.site.LocalUtility):
    interface.implements(IFireplace)
    
class Cave(BTreeContainer, grokcore.site.Site):
    grokcore.site.local_utility(Fireplace, public=True,
                                name_in_container='fireplace')

class Cave2(BTreeContainer, grokcore.site.Site):
    grokcore.site.local_utility(Fireplace, public=False,
                                name_in_container='fireplace')
