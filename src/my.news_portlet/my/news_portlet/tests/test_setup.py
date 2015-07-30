# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from plone import api
from my.news_portlet.testing import INTEGRATION_TESTING
import unittest2 as unittest

from plone.portlets.interfaces import IPortletType
from zope.component import getSiteManager, getUtilitiesFor, getUtility
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletType
from plone.app.portlets.interfaces import ILeftColumn, IRightColumn, IDashboard
from plone.app.portlets.tests.base import PortletsTestCase


class TestProductInstall(PortletsTestCase):

    def testPortletManagersRegistered(self):
        sm = getSiteManager(self.portal)
        registrations = [r.name for r in sm.registeredUtilities()
                            if IPortletManager == r.provided]
        self.assertEqual(['plone.dashboard1', 'plone.dashboard2',
                           'plone.dashboard3', 'plone.dashboard4',
                           'plone.footerportlets', 'plone.leftcolumn',
                           'plone.rightcolumn'], sorted(registrations))

    def testInterfaces(self):
        left = getUtility(IPortletManager, 'plone.leftcolumn')
        right = getUtility(IPortletManager, 'plone.rightcolumn')
        dashboard = getUtility(IPortletManager, 'plone.dashboard1')

        self.assertTrue(ILeftColumn.providedBy(left))
        self.assertTrue(IRightColumn.providedBy(right))
        self.assertTrue(IDashboard.providedBy(dashboard))

    def testAssignable(self):
        self.assertTrue(ILocalPortletAssignable.providedBy(self.folder))
        self.assertTrue(ILocalPortletAssignable.providedBy(self.portal))

    def testPortletTypesRegistered(self):
        portlets = [u[0] for u in getUtilitiesFor(IPortletType)]
        self.assertTrue('portlets.Classic' in portlets)
        self.assertTrue('portlets.Login' in portlets)

#def test_suite():
    #from unittest import TestSuite, makeSuite
    #suite = TestSuite()
    #suite.addTest(makeSuite(TestProductInstall))
    #return suite

class TestInstall(unittest.TestCase):
    """Test installation of my.news_portlet into Plone."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if my.news_portlet is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('my.news_portlet'))

    def test_uninstall(self):
        """Test if my.news_portlet is cleanly uninstalled."""
        self.installer.uninstallProducts(['my.news_portlet'])
        self.assertFalse(self.installer.isProductInstalled('my.news_portlet'))


