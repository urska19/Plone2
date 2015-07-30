import grokcore.view as grok

class NotAnInterfaceClass(object):
    grok.skin('failing_directive')
