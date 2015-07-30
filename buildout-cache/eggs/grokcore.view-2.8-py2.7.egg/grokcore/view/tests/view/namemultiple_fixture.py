"""
This should fail:
"""
import grokcore.view as grok

class MultipleNames(grok.View):
    grok.name('mammoth')
    grok.name('bear')
