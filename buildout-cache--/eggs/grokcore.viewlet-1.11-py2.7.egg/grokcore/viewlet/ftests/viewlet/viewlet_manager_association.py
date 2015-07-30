"""
We check whether viewlets automatically associate with a viewletmanager (if
only one of them is present).

Set up the model object to view::

  >>> root = getRootFolder()
  >>> root['cave'] = Cave()

Viewing the cave object should result in the viewlet being displayed::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/cave")
  >>> print browser.contents
  Me say HI

"""
import grokcore.viewlet as grok

class CavemenViewletManager(grok.ViewletManager):
    grok.name('manage.cavemen')

class FredViewlet(grok.Viewlet):
    def render(self):
        return u"Me say HI"

class Cave(grok.Context):
    pass

class Index(grok.View):
    pass
