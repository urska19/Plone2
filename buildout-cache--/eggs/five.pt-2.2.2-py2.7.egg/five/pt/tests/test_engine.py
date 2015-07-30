import os
import unittest

from Testing.ZopeTestCase import ZopeTestCase
from Testing.ZopeTestCase.sandbox import Sandboxed

path = os.path.dirname(__file__)

class TestPatches(Sandboxed, ZopeTestCase):
    def afterSetUp(self):
        from Products.Five import zcml
        import five.pt
        zcml.load_config("configure.zcml", five.pt)

    def test_pagetemplate(self):
        from Products.PageTemplates.PageTemplate import PageTemplate
        template = PageTemplate()

        # test rendering engine
        template.write(open(os.path.join(path, "simple.pt")).read())
        self.assertTrue('world' in template())

        # test arguments
        template.write(open(os.path.join(path, "options.pt")).read())
        self.assertTrue('Hello world' in template(greeting='Hello world'))

    def test_pagetemplatefile(self):
        from Products.PageTemplates.PageTemplateFile import PageTemplateFile

        # test rendering engine
        template = PageTemplateFile(os.path.join(path, "simple.pt"))
        template = template.__of__(self.folder)
        self.assertTrue('world' in template())

    def test_zopepagetemplate(self):
        from Products.PageTemplates.ZopePageTemplate import manage_addPageTemplate
        template = manage_addPageTemplate(self.folder, 'test')

        # aq-wrap before we proceed
        template = template.__of__(self.folder)

        # test rendering engine
        template.write(open(os.path.join(path, "simple.pt")).read())
        self.assertTrue('world' in template())

        # test arguments
        template.write(open(os.path.join(path, "options.pt")).read())
        self.assertTrue('Hello world' in template(
            greeting='Hello world'))

        # test commit
        import transaction
        transaction.commit()

def test_suite():
    import sys
    return unittest.findTestCases(sys.modules[__name__])
