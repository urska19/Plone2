"""
Content providers auto-associate with the context object that may be in a
module.

Set up the model object to view::

  >>> root = getRootFolder()
  >>> root['cave'] = cave = Cave()

We also set up another model that the content provider should not be auto-
associated with::

  >>> root['club'] = club = Club()

Let's get a content rpvoider associated with ``cave``::

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((cave, request), name='index')
  >>> from zope.contentprovider.interfaces import IContentProvider
  >>> mgr = component.getMultiAdapter((cave, request, view), IContentProvider,
  ...   'manage.cavemen')

We cannot get this content provider for ``club``, as there is none associated
with that as a context for the given name::

  >>> component.queryMultiAdapter((club, request, view), IContentProvider,
  ...   'manage.caveman') is None
  True

Ther is for one with a different name, using an explicit grok.context directive
however:

  >>> mgr = component.getMultiAdapter((club, request, view), IContentProvider,
  ...   'manage.clubmen')

"""

import zope.interface
import grokcore.view as grok
from context_fixture import Club

class CavemenContentProvider(grok.ContentProvider):
    grok.name('manage.cavemen')

    def render(self):
        pass

class Cave(grok.Context):
    pass

class Index(grok.View):
    grok.context(zope.interface.Interface)

    def render(self):
        return u"Hi"

class ClubContentProvider(grok.ContentProvider):
    grok.name('manage.clubmen')
    grok.context(Club)

    def render(self):
        pass
