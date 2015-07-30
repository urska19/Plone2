import unittest

from Products.Five import BrowserView
from Testing.ZopeTestCase import ZopeTestCase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SimpleView(BrowserView):
    index = ViewPageTemplateFile('simple.pt')


class LocalsView(BrowserView):
    def available(self):
        return 'yes'

    index = ViewPageTemplateFile('locals.pt')


class OptionsView(BrowserView):
    index = ViewPageTemplateFile('options.pt')


class SecureView(BrowserView):
    index = ViewPageTemplateFile('secure.pt')

    __allow_access_to_unprotected_subobjects__ = True

    def tagsoup(self):
        return '<foo></bar>'


class MissingView(BrowserView):
    index = ViewPageTemplateFile('missing.pt')


class TestPageTemplateFile(ZopeTestCase):
    def afterSetUp(self):
        from Products.Five import zcml
        import five.pt
        zcml.load_config("configure.zcml", five.pt)

    def test_simple(self):
        view = SimpleView(self.folder, self.folder.REQUEST)
        result = view.index()
        self.failUnless('Hello world!' in result)

    def test_secure(self):
        view = SecureView(self.folder, self.folder.REQUEST)
        from zExceptions import Unauthorized
        try:
            result = view.index()
        except Unauthorized:
            self.fail("Unexpected exception.")
        else:
            self.failUnless('&lt;foo&gt;&lt;/bar&gt;' in result)

    def test_locals(self):
        view = LocalsView(self.folder, self.folder.REQUEST)
        result = view.index()
        self.failUnless("view:yes" in result)
        #self.failUnless('Folder at test_folder_1_' in result)
        #self.failUnless('http://nohost' in result)
        self.failUnless('here==context:True' in result)
        self.failUnless('here==container:True' in result)
        self.failUnless("root:(\'\',)" in result)
        self.failUnless("nothing:" in result)
        self.failUnless("rfc822" in result)

    def test_options(self):
        view = OptionsView(self.folder, self.folder.REQUEST)
        options = dict(
            a=1,
            b=2,
            c='abc',
        )
        result = view.index(**options)
        self.failUnless("a : 1" in result)
        self.failUnless("c : abc" in result)

    def test_MissingValue(self):
        request = self.folder.REQUEST
        view = MissingView(self.folder, request)

        from zope.component import provideUtility
        from zope.i18n.interfaces import ITranslationDomain
        from zope.i18n.simpletranslationdomain import SimpleTranslationDomain
        pfp = SimpleTranslationDomain('test', {})
        provideUtility(pfp, ITranslationDomain, name='test')

        import Missing
        request["LANGUAGE"] = 'en'
        result = view.index(missing=Missing.MV)
        del request.other["LANGUAGE"]

        self.failUnless('<span></span>' in result)


def test_suite():
    import sys
    return unittest.findTestCases(sys.modules[__name__])
