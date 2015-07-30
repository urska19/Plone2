"""
We check here that specifying grok.view() on module level works.
grok.view() on module level will make the content provider be associated
with the CaveView, so nothing is found for BoneView and an error should
occur.

Set up a content object in the application root:

  >>> root = getRootFolder()
  >>> root['fred'] = Fred()
  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False

This view does have the content provider registered for:

  >>> browser.open("http://localhost/fred/@@caveview")
  >>> browser.contents
  'Cave'

However, the boneview does not have a content provider registered for:

  >>> browser.open("http://localhost/fred/@@boneview")
  Traceback (most recent call last):
  ...
  ContentProviderLookupError: cave

And the potview again does, by way of a component-level grok.view directive:

  >>> browser.open("http://localhost/fred/@@potview")
  >>> browser.contents
  'Pot'

"""

import grokcore.view as grok

class Fred(grok.Context):
    pass

class CaveView(grok.View):

    def render(self):
        return u"Cave"

grok.view(CaveView)

class BoneView(grok.View):
    pass

class CaveContentProvider(grok.ContentProvider):
    grok.name('cave')

    def render(self):
        pass

class PotView(grok.View):

    def render(self):
        return u"Pot"

class PotCaveContentProvider(CaveContentProvider):
    grok.view(PotView)
