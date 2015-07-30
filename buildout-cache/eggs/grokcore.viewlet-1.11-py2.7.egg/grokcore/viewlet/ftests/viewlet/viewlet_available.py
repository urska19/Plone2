"""

===================
Viewlet availablity
===================

The viewlet manager will filter out "unavailable" viewlets before rendering.
The availability of a viewlet is determined by calling available() on the
individuel viewlet. Note that the availability check is performed *after* the
update() is caled on the viewlet, but *before* the render() is called.

Set up a content object in the application root::

  >>> root = getRootFolder()
  >>> root['wilma'] = CaveWoman()

Traverse to the view on the model object and render the viewlets "Brack Bone"
and "T-Rex Bone", but not the "Elephant Bone":

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/wilma/@@bonesview")
  >>> print browser.contents
  Brack Bone
  T-Rex Bone

At some point in time, the Sabre Tooth Bone becomes availalble:

  >>> SabreToothBone._available = True
  >>> browser.open("http://localhost/wilma/@@bonesview")
  >>> print browser.contents
  Brack Bone
  Sabre Tooth Bone
  T-Rex Bone

The availability can depend on some flag available in the request and since the
update() of a viewlet is called before the check, the availability can be
computed as wel.

First it is there:

  >>> browser.open("http://localhost/wilma/@@bonesview?requestcounting=true")
  >>> print browser.contents
  Brack Bone
  Only for every other request!
  Sabre Tooth Bone
  T-Rex Bone

Next request it is not:

  >>> browser.open("http://localhost/wilma/@@bonesview?requestcounting=true")
  >>> print browser.contents
  Brack Bone
  Sabre Tooth Bone
  T-Rex Bone

And then we have it again:

  >>> browser.open("http://localhost/wilma/@@bonesview?requestcounting=true")
  >>> print browser.contents
  Brack Bone
  Only for every other request!
  Sabre Tooth Bone
  T-Rex Bone

"""


import grokcore.viewlet as grok
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class CaveWoman(grok.Context):
    pass

class BonesView(grok.View):
    grok.context(Interface)

class Bones(grok.ViewletManager):
    grok.context(Interface)
    grok.name('bones')

class BrackerBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Bones)

    def render(self):
        return u"Brack Bone"

class TRexBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Bones)

    def render(self):
        return u"T-Rex Bone"

class ElephantBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Bones)

    def available(self):
        # This type of bone has not evolved just yet.
        return False

    def render(self):
        return u"Elephant Bone"

class SabreToothBone(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(Bones)

    _available = False

    def available(self):
        return self._available

    def render(self):
        return u"Sabre Tooth Bone"

class OnlyForEvenRequest(grok.Viewlet):
    # Convoluted example of a viewlet that is available only for every
    # other request, but only when we're indicating that we're counting
    # requests.

    count = 1

    def update(self):
        if 'requestcounting' in self.request.form:
            OnlyForEvenRequest.count += 1

    def available(self):
        if not self.count % 2:
            return True
        return False

    def render(self):
        return u"Only for every other request!"
