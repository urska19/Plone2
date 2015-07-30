"""
This should issue a UserWarning.
"""
import grokcore.view as grok
from first_module import Mammoth

grok.templatedir("templates")

class Food(grok.View):
    grok.context(Mammoth)

