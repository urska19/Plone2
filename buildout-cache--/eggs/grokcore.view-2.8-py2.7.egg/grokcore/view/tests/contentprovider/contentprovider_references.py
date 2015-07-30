"""
A grok.ContentProvider instance has references to the components it was
registered for::

  >>> grok.testing.grok(__name__)
  >>> from zope import component
  >>> from zope.contentprovider.interfaces import IContentProvider
  >>> from zope.publisher.browser import TestRequest
  >>> ctxt = AContext()
  >>> request = TestRequest()
  >>> view = component.getMultiAdapter((ctxt, request), name='a_view')
  >>> provider = component.getMultiAdapter(
  ...     (ctxt, request, view), IContentProvider, name='a_content_provider')
  >>> provider.context is ctxt
  True

  >>> provider.view is view
  True

  >>> provider.request is request
  True

  >>> provider.render()
  u'I provide some content for a view'

"""

import grokcore.view as grok

class AContext(grok.Context):
    pass

class AView(grok.View):
    grok.name('a_view')

    def render(self):
        return u""

class AContentProvider(grok.ContentProvider):
    grok.name('a_content_provider')

    def render(self):
        return u"I provide some content for a view"