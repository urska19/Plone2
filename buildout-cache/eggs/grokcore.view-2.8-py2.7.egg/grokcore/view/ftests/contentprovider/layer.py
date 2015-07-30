"""
Content providers can be discriminated based on layer too::

  >>> root = getRootFolder()
  >>> root['wilma'] = CaveWoman()

Traverse to the view on the model object. We get the content provider
registered for the default layer::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/wilma/@@caveview")
  >>> print browser.contents
  Soup pot

Traverse to the view on the model object. We get the content provider
registered for the "boneskin" layer::

  >>> browser.open("http://localhost/++skin++boneskin/wilma/@@caveview")
  >>> print browser.contents
  Layered pot

"""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
import grokcore.view as grok

class CaveWoman(grok.Context):
    pass

class CaveView(grok.View):
    grok.context(Interface)

class Pot(grok.ContentProvider):
    grok.context(Interface)

    def render(self):
        return u"Soup pot"

class IBoneLayer(IDefaultBrowserLayer):
    grok.skin('boneskin')

class LayeredPot(grok.ContentProvider):
    grok.name('pot')
    grok.context(Interface)
    grok.layer(IBoneLayer)

    def render(self):
        return u"Layered pot"
