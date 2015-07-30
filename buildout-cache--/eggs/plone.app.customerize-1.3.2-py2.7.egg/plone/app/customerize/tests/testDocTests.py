import doctest
from unittest2 import TestCase
from unittest2 import TestSuite

from Testing.ZopeTestCase import FunctionalDocFileSuite

from plone.testing.z2 import Browser

from plone.app.customerize.testing import \
    PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING


class CustomerizeFunctionalTestCase(TestCase):

    layer = PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.app.acl_users.userFolderAddUser('app', 'secret', ['Manager'], [])

        import transaction
        transaction.commit()

        self.site_administrator_browser = Browser(self.app)
        self.site_administrator_browser.handleErrors = False
        self.site_administrator_browser.addHeader(
            'Authorization',
            'Basic %s:%s' % ('app', 'secret')
        )


def test_suite():
    suite = TestSuite()
    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    for testfile in ('testBrowserLayers.txt', 'testCustomizeView.txt'):
        suite.addTest(FunctionalDocFileSuite(testfile,
                                optionflags=OPTIONFLAGS,
                                package="plone.app.customerize.tests",
                                test_class=CustomerizeFunctionalTestCase),
                     )
    return suite
