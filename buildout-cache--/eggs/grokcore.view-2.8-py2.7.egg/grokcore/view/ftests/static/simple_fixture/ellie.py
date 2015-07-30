import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class Index(grok.View):
    pass

index = grok.PageTemplate("""\
<html>
<body>
<a tal:attributes="href static/file.txt">Some text in a file</a>
</body>
</html>""")
