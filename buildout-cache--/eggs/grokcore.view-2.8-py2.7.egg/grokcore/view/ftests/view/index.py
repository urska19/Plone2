"""
  >>> getRootFolder()["manfred"] = Mammoth()

The default view name for a model is 'index':

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/manfred")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hello, world!</h1>
  <span><class 'grokcore.view.ftests.view.index.Mammoth'></span>
  <span><class 'grokcore.view.ftests.view.index.Mammoth'></span>
  </body>
  </html>

"""
import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class Index(grok.View):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<h1>Hello, world!</h1>
<span tal:content="structure python:context.__class__">green</span>
<span tal:content="structure context/__class__">green</span>
</body>
</html>
""")
