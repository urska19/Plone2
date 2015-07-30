"""

  >>> grok.testing.grok('grokcore.view.tests.view.cross_package_fixture')

  >>> from grokcore.view import template
  >>> from cross_package_fixture import zbase
  >>> from cross_package_fixture.subpackage import sub
  >>> from cross_package_fixture.subpackage import subtemplatedir

  >>> template.bind().get(zbase.BaseView)
  ('grokcore.view.tests.view.cross_package_fixture.zbase', 'basetemplate')

  >>> template.bind().get(sub.SubView)
  ('grokcore.view.tests.view.cross_package_fixture.zbase', 'basetemplate')

  >>> template.bind().get(sub.SubViewOverrideTemplate)
  ('grokcore.view.tests.view.cross_package_fixture.subpackage.sub',
   'subtemplate')

  >>> template.bind().get(subtemplatedir.MoreSubView)
  ('grokcore.view.tests.view.cross_package_fixture.zbase', 'basetemplate')

  >>> template.bind().get(subtemplatedir.MoreSubViewOverrideTemplate)
  ('grokcore.view.tests.view.cross_package_fixture.subpackage.subtemplatedir',
   'moretemplate')


"""
import grokcore.view as grok
