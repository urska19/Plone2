import grokcore.view as grok

class BaseView(grok.View):
    grok.template('basetemplate')
    grok.context(object)
