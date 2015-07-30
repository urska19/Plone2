"""
Let's check that the viewlet namespaces are correct. In particular,
``view`` in a template should refer to the namespace of the view the
viewlet is registered for, not the actual viewlet itself.

  >>> root = getRootFolder()
  >>> root['cave'] = Cave()

Let's look at the first template, which includes the viewlet::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/cave/@@index")
  >>> print browser.contents
  <grokcore.viewlet.ftests.viewlet.template_namespaces.Cave object at ...>
  <grokcore.viewlet.ftests.viewlet.template_namespaces.Index object at ...>
  <grokcore.viewlet.ftests.viewlet.template_namespaces.MirandaViewlet object at ...>
  <grokcore.viewlet.ftests.viewlet.template_namespaces.CavewomenViewletManager object at ...>

This is indeed what we expected from the viewlet.

Let's look at a template for the viewlet manager too::

  >>> browser.open("http://localhost/cave/@@necklace")
  >>> print browser.contents
  <grokcore.viewlet.ftests.viewlet.template_namespaces.Cave object at ...>
  <grokcore.viewlet.ftests.viewlet.template_namespaces.Necklace object at ...>
  <grokcore.viewlet.ftests.viewlet.template_namespaces.CavewomenViewletManagerWithTemplate object at ...>

"""
import grokcore.viewlet as grok


class Cave(grok.Context):
    pass

class Index(grok.View):
    pass

class CavewomenViewletManager(grok.ViewletManager):
    grok.name('manage.cavewomen')
    grok.view(Index)

class MirandaViewlet(grok.Viewlet):
    grok.template('mirandaviewlet')
    grok.view(Index)
    grok.viewletmanager(CavewomenViewletManager)

class Necklace(grok.View):
    pass

class CavewomenViewletManagerWithTemplate(grok.ViewletManager):
    grok.name('manage.cavewomenwithtemplate')
    grok.template('mirandaviewletmanager')
    grok.view(Necklace)
