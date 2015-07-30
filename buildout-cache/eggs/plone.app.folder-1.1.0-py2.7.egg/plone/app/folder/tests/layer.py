# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing.bbb import PTC_FUNCTIONAL_TESTING

from plone.folder.partial import PartialOrdering

from zope.component import provideAdapter


class IntegrationFixture(PloneSandboxLayer):
    """ layer for integration tests using the folder replacement type """

    defaultBases = (PTC_FUNCTIONAL_TESTING,)

    def setUpZope(self, app, configurationContext):
        from plone.app.folder import tests
        self.loadZCML('testing.zcml', package=tests)

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")


PAF_INTEGRATION_FIXTURE = IntegrationFixture()
IntegrationLayer = FunctionalTesting(
    bases=(PAF_INTEGRATION_FIXTURE,), name='plone.app.folder testing:Integration')


class PartialOrderingIntegrationFixture(IntegrationFixture):
    """ layer for integration tests using the partial ordering adapter """

    def setUpZope(self, app, configurationContext):
        IntegrationFixture.setUpZope(self, app, configurationContext)
        provideAdapter(PartialOrdering)


PAF_ORDERING_FIXTURE = PartialOrderingIntegrationFixture()
PartialOrderingIntegrationLayer = FunctionalTesting(
    bases=(PAF_ORDERING_FIXTURE,), name='plone.app.folder testing:Partial ordering integration')
