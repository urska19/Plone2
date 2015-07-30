# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from plone import api
from dexterityurska.site.testing import INTEGRATION_TESTING
import unittest2 as unittest


class TestInstall(unittest.TestCase):
    """Test installation of dexterityurska into Plone."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if dexterityurska is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('dexterityurska.site'))

    def test_uninstall(self):
        """Test if dexterityurska is cleanly uninstalled."""
        self.installer.uninstallProducts(['dexterityurska.site'])
        self.assertFalse(self.installer.isProductInstalled('dexterityurska.site'))

