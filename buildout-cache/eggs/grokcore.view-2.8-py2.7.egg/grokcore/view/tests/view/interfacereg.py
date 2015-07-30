"""
Views can also provide an interface, in which case they can be looked up (via
getMultiAdapter) on the interface. This approach is a bit more explicit than
requiring all views to have a certain name, since this is an interface/contract
rather than an arbitrary naming standard.

First, do some initialization

  >>> grok.testing.grok(__name__)
  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component

If grok.name is used, it needs to be supplied. If not supplied, grok.name
defaults to the lowercase of the class:

  >>> view = component.getMultiAdapter((manfred, request), name='cavepainting')
  >>> view()
  'a chalk cave painting'

It is also possible to look up the same view by also including the interface:

  >>> view = component.getMultiAdapter(
  ...     (manfred, request), interface=IChalk, name='cavepainting')
  >>> view()
  'a chalk cave painting'

The name can be set to '', in which case it is an 'unnamed' view:

  >>> view = component.getMultiAdapter((manfred, request), interface=IRealist)
  >>> view()
  'a realist cave painting'

Multipl IPaintStyles can now be looked up by interface, rather than name:

  >>> view = component.getMultiAdapter(
  ...     (manfred, request), interface=IImpressionist)
  >>> view()
  'an impressionist cave painting'

"""

import grokcore.view as grok
from zope.interface import Interface

class Mammoth(grok.Context):
    pass

class IPaintStyle(Interface):
    pass

class IChalk(IPaintStyle):
    pass

class IImpressionist(IPaintStyle):
    pass

class IRealist(IPaintStyle):
    pass

class CavePainting(grok.View):
    grok.provides(IChalk)

    def render(self):
        return "a chalk cave painting"

class ImpressionistCavePainting(grok.View):
    grok.provides(IImpressionist)
    grok.name('')

    def render(self):
        return "an impressionist cave painting"

class RealistCavePainting(grok.View):
    grok.provides(IRealist)
    grok.name('')

    def render(self):
        return "a realist cave painting"
