# -*- coding: utf-8 -*-
from Products.CMFCore.permissions import setDefaultRoles
from zope.i18nmessageid import MessageFactory

PloneMessageFactory = MessageFactory('plone')

setDefaultRoles(
    'plone.portlet.static: Add static portlet',
    ('Manager', 'Site Administrator', 'Owner', )
)
