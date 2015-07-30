from pkg_resources import resource_stream
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing.z2 import Browser
from dexterityurska.site.testing import FUNCTIONAL_TESTING
from dexterityurska.site.testing import INTEGRATION_TESTING
from zope.component import createObject
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
import unittest

class MyIntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='vehicle_card')
        self.assertTrue(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='vehicle_card')
        schema = fti.lookupSchema()
        self.assertTrue(schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='vehicle_card')
        factory = fti.factory
        vehicle_card = createObject(factory)
        self.assertTrue(vehicle_card)

    def test_adding(self):
        self.portal.invokeFactory('vehicle_card', 'vehicle_card')
        self.assertTrue(self.portal.vehicle_card)


class MyFunctionalTest(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        # Set up browser
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )
##ID
    #def test_add(self):
        #self.browser.open(self.portal_url + '/++add++vehicle_card')
        #ctrl = self.browser.getControl
        #ctrl(name="form.widgets.title").value = "New Car"
        ##ctrl(name="form.widgets.of_passengers").value = '1'
        #ctrl(name="form.widgets.properties:list").value = ["Gas", "Van"]
        #img_ctrl = ctrl(name="form.widgets.image")
        #img_ctrl.add_file(resource_stream(__name__, 'plone.png'),
                          #'image/png', 'plone.png')
        #ctrl("Save").click()

        ##vehicle_card = self.portal.['my-vehicle_card']
        

        #self.assertEqual("New Car", self.portal['my-vehicle_card'].title)
        ##self.assertEqual('1',vehicle_card.of_passengers)
        #self.assertEqual({'Gas', 'Van'}, self.portal['my-vehicle_card'].properties)
        #self.assertEqual((491, 128), self.portal['my-vehicle_card'].image.getImageSize())        

    def test_view(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            "vehicle_card",
            id="vehicle_card",
            title="New Car",
        )

        import transaction
        transaction.commit()

        self.browser.open(self.portal_url + '/vehicle_card')

        self.assertTrue('New Car' in self.browser.contents)

