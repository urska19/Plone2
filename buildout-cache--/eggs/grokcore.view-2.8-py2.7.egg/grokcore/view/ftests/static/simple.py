"""
We use a special name 'static' in page templates to allow easy linking
to resources.

In the context of a grok application, you can use fanstatic (through zope.fanstatic)
instead of the dummy implementation in this test:

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> root = getRootFolder()
  >>> from grokcore.view.ftests.static.simple_fixture.ellie import Mammoth
  >>> root[u'ellie'] = Mammoth()
  >>> browser.open('http://localhost/ellie')
  >>> print browser.contents
  <html>
  <body>
  <a href="dummy:/file.txt">Some text in a file</a>
  </body>
  </html>

"""
import zope.interface
import zope.component

from zope.traversing.interfaces import ITraversable
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.publisher.interfaces.browser import IBrowserRequest

class DummyResource(object):
    """ Dummy resource implementation. """
    zope.interface.implements(ITraversable, IAbsoluteURL)

    def __init__(self, request, name=''):
        self.request = request
        self.name = name

    def traverse(self, name, furtherPath):
        name = '%s/%s' % (self.name, name)
        return DummyResource(self.request, name=name)

    def __str__(self):
        return 'dummy:%s' % self.name

zope.component.provideAdapter(factory=DummyResource,
    adapts=(IBrowserRequest,),
    provides=zope.interface.Interface,
    name='grokcore.view.ftests.static.simple_fixture')
