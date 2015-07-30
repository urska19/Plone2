"""
We check here that the grok.viewletmanager directive works on
module level. If we don't specify a viewlet manager at all for
the Fred viewlet we get an error, so if we specify a manager using
the directive on module level we shouldn't get any error.

Set up a content object in the application root::

  >>> root = getRootFolder()
  >>> root['fred'] = Fred()

Traverse to the view on the model object. We get the viewlets
registered for the default layer, with the anybody permission::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/fred/@@boneview")
  >>> print browser.contents
  Fred viewlet

"""

import grokcore.viewlet as grok

class Fred(grok.Context):
    pass

class BoneView(grok.View):
    pass

class BoneManager(grok.ViewletManager):
    grok.name('bone')

class CaveManager(grok.ViewletManager):
    grok.name('cave')

grok.viewletmanager(CaveManager)

class FredViewlet(grok.Viewlet):
    def render(self):
        return u"Fred viewlet"
