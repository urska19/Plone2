"""
A viewlet is not allowed to define its own render method and have a template
associated with it at the same time.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
    ...
  ConfigurationExecutionError: martian.error.GrokError: Multiple possible ways to render viewlet <class 'grokcore.viewlet.tests.viewlet.viewlet_render_and_template.Viewlet'>. It has both a 'render' method as well as an associated template.
  in:

"""

import grokcore.viewlet as grok
from zope.interface import Interface


class ViewletManager(grok.ViewletManager):
    grok.name('foo')
    grok.context(Interface)


class Viewlet(grok.Viewlet):
    grok.viewletmanager(ViewletManager)
    grok.context(Interface)

    def render(self):
        return u"Render method but also a template!"
