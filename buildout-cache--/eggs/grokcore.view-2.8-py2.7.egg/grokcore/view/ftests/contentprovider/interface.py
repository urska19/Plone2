"""
Verify that associating a content provider with an view interface instead of
with a view class works as expected.

Set up the model object to view::

  >>> root = getRootFolder()
  >>> root['cave'] = Cave()

Viewing the cave object should result in the content provider being displayed,
as it is associated with the view's interface::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/cave")
  >>> print browser.contents
  Hi

  >>> browser.open("http://localhost/cave/@@secondindex")
  >>> print browser.contents
  Hi

"""

from zope.interface import Interface
import grokcore.view as grok

class Cave(grok.Context):
    pass

class ICavemenView(Interface):
    pass

class Index(grok.View):
    grok.implements(ICavemenView)

class CavemenContentProvider(grok.ContentProvider):
    grok.name('manage.cavemen')
    grok.view(ICavemenView)

    def render(self):
        return u'Hi'

class SecondIndex(grok.View):
    grok.implements(ICavemenView)

    def render(self):
        return u'Hi'
