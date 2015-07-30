from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import dexterityurska.site


class DexterityurskaSiteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            dexterityurska.site,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'dexterityurska.site:default')


FIXTURE = DexterityurskaSiteLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='DexterityurskaSiteLayer:IntegrationTesting'
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='DexterityurskaSiteLayer:FunctionalTesting'
)


