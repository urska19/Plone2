"""
You can subscribe to events using the @grok.subscribe decorator:

  >>> grok.testing.grok(__name__)
  >>> manfred = Mammoth('Manfred')
  >>> zope.event.notify(ObjectEvent(manfred))
  >>> mammoths
  ['Manfred']
  >>> mammoths2
  ['Manfred']

The decorated event handling function can also be called directly:

  >>> mammothAdded(Mammoth('Max'),None)
  >>> mammoths
  ['Manfred', 'Max']

"""
import zope.event
import grokcore.component as grok
from zope.component.interfaces import IObjectEvent, ObjectEvent

class Mammoth(object):
    def __init__(self, name):
        self.name = name

mammoths = []
mammoths2 = []

@grok.subscribe(Mammoth, IObjectEvent)
def mammothAdded(mammoth, event):
    mammoths.append(mammoth.name)

@grok.subscribe(Mammoth, IObjectEvent)
def mammothAddedInstance(mammoth, event):
    mammoths2.append(mammoth.name)
