import grokcore.view as grok


class Skin1(grok.IBrowserRequest):
    grok.skin('foo')
    grok.skin('bar')
