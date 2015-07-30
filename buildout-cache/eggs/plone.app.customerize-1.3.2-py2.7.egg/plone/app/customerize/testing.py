# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneFixture
from zope.configuration import xmlconfig


class PloneAppCustomerize(PloneFixture):

    def setUpZCML(self):
        super(PloneAppCustomerize, self).setUpZCML()

        import plone.app.customerize
        xmlconfig.file('configure.zcml',
                       plone.app.customerize,
                       context=self['configurationContext'])
        xmlconfig.file('testing.zcml',
                       plone.app.customerize.tests,
                       context=self['configurationContext'])
        xmlconfig.file('duplicate_viewlet.zcml',
                       plone.app.customerize.tests,
                       context=self['configurationContext'])


PLONE_APP_CUSTOMERIZE_FIXTURE = PloneAppCustomerize()
PLONE_APP_CUSTOMERIZE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_CUSTOMERIZE_FIXTURE,),
    name="PloneAppCustomerize:Functional",
)
