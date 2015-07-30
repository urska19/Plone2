# -*- coding: utf-8 -*-
## CMFPlacefulWorkflow
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
CMFPlacefulWorkflow TestCase module
"""
__docformat__ = 'restructuredtext'

# Zope imports
from Products.CMFCore.interfaces import ISiteRoot
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

# Plone imports
from plone.app.testing.bbb import PloneTestCase
from plone.app.testing.bbb import PloneTestCaseFixture
from plone.testing import z2
from plone.app import testing


class PlacefulWorkflowLayer(PloneTestCaseFixture):

    def setUpZope(self, app, configurationContext):
        super(PlacefulWorkflowLayer, self).setUpZope(app, configurationContext)
        profile_registry.registerProfile(
            name='exportimport', title='Test Placeful Workflow Profile',
            description=(
                "Tests the placeful workflow policy handler."),
            path='profiles/exportimport',
            product='Products.CMFPlacefulWorkflow.tests',
            profile_type=EXTENSION, for_=ISiteRoot)
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        super(PlacefulWorkflowLayer, self).setUpPloneSite(portal)
        # install sunburst theme
        testing.applyProfile(portal, 'Products.CMFPlacefulWorkflow:CMFPlacefulWorkflow')

    def tearDownZope(self, app):
        super(PlacefulWorkflowLayer, self).tearDownZope(app)
        z2.uninstallProduct(app, 'Products.CMFPlacefulWorkflow')

PWF_FIXTURE = PlacefulWorkflowLayer()
PWF_LAYER = testing.FunctionalTesting(bases=(PWF_FIXTURE, ),
        name='PlacefulWorkflowTestCase:Functional')


class CMFPlacefulWorkflowTestCase(PloneTestCase):

    layer = PWF_LAYER

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

    def getPermissionsOfRole(self, role):
        perms = self.portal.permissionsOfRole(role)
        return [p['name'] for p in perms if p['selected']]

CMFPlacefulWorkflowFunctionalTestCase = CMFPlacefulWorkflowTestCase
