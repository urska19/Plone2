# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting


class PloneThemeLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import plone.theme.tests
        self.loadZCML('tests.zcml', package=plone.theme.tests)

PLONETHEME_FIXTURE = PloneThemeLayer()

PLONETHEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONETHEME_FIXTURE,),
    name="PloneTheme:Functional")

PLONETHEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONETHEME_FIXTURE,),
    name="PloneTheme:Integration")
