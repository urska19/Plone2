

from grokcore import view as grok


class Cave(grok.Context):
    pass


class StaticResource(grok.DirectoryResource):
    grok.name('grokcore.view.ftests.static.templates_nooverridestatic.original')
    grok.path('static')


class CaveView(grok.View):
    grok.context(Cave)
