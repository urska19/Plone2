import grokcore.view as grok


grok.templatedir("templates")

class Mammoth(grok.Context):
    pass

class CavePainting(grok.View):
    pass

unassociated_instance = grok.PageTemplate("""
<html><body><h1>GROK PAINT MAMMOTH!</h1></body></html>
""")
