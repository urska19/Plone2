"""
  >>> getRootFolder()["manfred"] = Mammoth()

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/++skin++casual/manfred/@@hello")
  >>> print browser.contents
  <html>
  <body>
  <h1>Hi sir !</h1>
  </body>
  </html>

  >>> browser.open("http://localhost/++skin++party/manfred/@@happy")
  >>> print browser.contents
  Hee yay !

  >>> browser.open("http://localhost/++skin++rainy/manfred/@@sad")
  >>> print browser.contents
  Aw... It rains.

"""
import grokcore.view as grok


class CasualLayer(grok.IBrowserRequest):
    pass


class PartyLayer(grok.IBrowserRequest):
    pass


class RainyLayer(grok.IBrowserRequest):
    pass


class PartySkin(PartyLayer):
    grok.skin('party')


class CasualSkin(CasualLayer):
    grok.skin('casual')


class RainySkin(RainyLayer):
    grok.skin('rainy')


grok.layer(CasualLayer)


class Mammoth(grok.Context):
    pass


class Hello(grok.View):
    pass


hello = grok.PageTemplate("""\
<html>
<body>
<h1>Hi sir !</h1>
</body>
</html>
""")


class Happy(grok.View):
    grok.layer(PartyLayer)

    def render(self):
        return u"Hee yay !"


class Sad(grok.View):
    grok.layer(RainyLayer)

    def render(self):
        return u"Aw... It rains."
