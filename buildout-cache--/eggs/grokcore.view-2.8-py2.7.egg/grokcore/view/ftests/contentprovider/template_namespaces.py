"""
Let's check that the contentprovider namespaces are correct. In
particular, ``view`` in a template should refer to the view the content
provider is registered for, not the provider itself.

  >>> root = getRootFolder()
  >>> root['cave'] = Cave()

Let's look at the first template, which includes the content provider:

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/cave/@@index")
  >>> print browser.contents
  <grokcore.view.ftests.contentprovider.template_namespaces.Cave object at ...>
  <grokcore.view.ftests.contentprovider.template_namespaces.Index object at ...>
  <grokcore.view.ftests.contentprovider.template_namespaces.CavewomenContentProvider object at ...>

This is indeed what we expected from the content provider.

Let's look at a template for too:

  >>> browser.open("http://localhost/cave/@@necklace")
  >>> print browser.contents
  <grokcore.view.ftests.contentprovider.template_namespaces.Cave object at ...>
  <grokcore.view.ftests.contentprovider.template_namespaces.Necklace object at ...>
  <grokcore.view.ftests.contentprovider.template_namespaces.CavewomenContentProviderWithTemplate object at ...>

"""
import grokcore.view as grok

class Cave(grok.Context):
    pass

class Index(grok.View):
    pass

class CavewomenContentProvider(grok.ContentProvider):
    grok.name('manage.cavewomen')
    grok.view(Index)

    def render(self):
        return u'%r %r %r' % (self.context, self.view, self)

class Necklace(grok.View):
    pass

class CavewomenContentProviderWithTemplate(grok.ContentProvider):
    grok.name('manage.cavewomenwithtemplate')
    grok.template('mirandaprovider')
    grok.view(Necklace)
