"""
A content provider is not allowed to define its own render method and
have a template associated with it at the same time.

  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
   ...
  ConfigurationExecutionError: martian.error.GrokError: Multiple possible ways
  to render contentprovider <class 'grokcore.view.tests.contentprovider.contentprovider_render_and_template.ContentProvider'>.
  It has both a 'render' method as well as an associated template.
  in:

"""

from zope.interface import Interface
import grokcore.view as grok

grok.templatedir('render_and_template_templates')

class ContentProvider(grok.ContentProvider):
    grok.name('foo')
    grok.context(Interface)
    grok.template('contentprovider')

    def render(self):
        """There's also a template!
        """
