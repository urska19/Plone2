"""
You cannot use local_utility with 'public' set to True if the site class
isn't a container:

  >>> grokcore.site.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  GrokError: Cannot set public to True with grok.local_utility as the site
  (<class 'grokcore.site.tests.utility.publicnoncontainer.Cave'>) is not a container.

"""
import grokcore.site

from zope import interface

class IFireplace(interface.Interface):
    pass

class Fireplace(grokcore.site.LocalUtility):
    interface.implements(IFireplace)
    
class Cave(grokcore.site.Site):
    grokcore.site.local_utility(Fireplace, public=True,
                                name_in_container='fireplace')
