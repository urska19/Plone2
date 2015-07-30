import grokcore.view as grok
from grokcore.view.tests.view.cross_package_fixture.zbase import BaseView

grok.templatedir('more_templates')

class MoreSubView(BaseView):
    pass

class MoreSubViewOverrideTemplate(BaseView):
    grok.template('moretemplate')