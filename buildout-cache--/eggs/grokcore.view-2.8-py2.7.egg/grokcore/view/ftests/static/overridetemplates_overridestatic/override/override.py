

from grokcore import view as grok
from grokcore.view.ftests.static.overridetemplates_overridestatic.original.original import CaveView


class StaticResource(grok.DirectoryResource):
    grok.name('grokcore.view.ftests.static.overridetemplates_overridestatic.override')
    grok.path('static')


class PalaceView(CaveView):
    pass
