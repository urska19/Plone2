# -*- coding: utf-8 -*-

# helper module to ease setting up backward-compatibility tests for
# ATContentTypes and CMFPlone

from Products.Five import fiveconfigure
from Testing.ZopeTestCase import installPackage
from Testing.ZopeTestCase import installProduct
from Zope2.App.zcml import load_config

installProduct('Five', quiet=True)

fiveconfigure.debug_mode = True

import plone.app.folder

load_config('configure.zcml', plone.app.folder)
fiveconfigure.debug_mode = False

installPackage('plone.app.folder', quiet=True)
