"""
You can explicitly specify the template directory using grok.templatedir on module level:

  >>> grok.testing.grok(__name__)

  >>> manfred = Mammoth()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> from zope import component
  >>> view = component.getMultiAdapter((manfred, request), name='food')
  >>> print view()
  <html>
  <body>
  ME GROK EAT MAMMOTH!
  </body>
  </html>

"""
import grokcore.view as grok

grok.templatedir('templatedirectoryname')

class Mammoth(grok.Context):
    pass

class Food(grok.View):
    pass
