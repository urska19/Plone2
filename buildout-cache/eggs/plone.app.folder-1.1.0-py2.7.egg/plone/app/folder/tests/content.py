# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from OFS.interfaces import IOrderedContainer
from Products.ATContentTypes.config import PROJECTNAME
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interface import IATFolder
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.permission import permissions
from Products.Archetypes.atapi import BaseFolder
from Products.CMFCore.utils import getToolByName
from plone.app.folder.base import BaseBTreeFolder
from plone.folder.interfaces import IOrderable
from zope.event import notify
from zope.interface import implementer
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent import ObjectModifiedEvent


ATFolderSchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema
finalizeATCTSchema(ATFolderSchema, folderish=True, moveDiscussion=False)


class UnorderedFolder(BaseFolder):
    """ sample unordered (old-style) folder for testing purposes """

    def SearchableText(self):
        return ''


@implementer(IOrderable)
class OrderableFolder(BaseBTreeFolder):
    """ sample ordered btree-based folder (needing the interface) """


@implementer(IATFolder, IOrderedContainer)
class NonBTreeFolder(ATCTOrderedFolder):
    """ an old-style folder much like `ATFolder` before Plone 4;  this is
        a reduced version of `ATContentTypes.content.folder.ATFolder` """

    schema = ATFolderSchema
    portal_type = 'NonBTreeFolder'
    archetype_name = 'NonBTreeFolder'
    security = ClassSecurityInfo()

permissions['NonBTreeFolder'] = PROJECTNAME + ': ATFolder'
registerATCT(NonBTreeFolder, PROJECTNAME)


def addNonBTreeFolder(container, id, **kwargs):
    """ at-constructor copied from ClassGen.py """
    obj = NonBTreeFolder(id)
    notify(ObjectCreatedEvent(obj))
    container._setObject(id, obj)
    obj = container._getOb(id)
    obj.initializeArchetype(**kwargs)
    notify(ObjectModifiedEvent(obj))
    return obj


def _createObjectByType(type_name, container, cid, *args, **kw):
    """Create an object without performing security checks

    Note
        copied from ``Products.CMFPlone.utils._createObjectByType`` because
        this was this import was the only dependency on CMFPlone!

    invokeFactory and fti.constructInstance perform some security checks
    before creating the object. Use this function instead if you need to
    skip these checks.

    This method uses
    CMFCore.TypesTool.FactoryTypeInformation._constructInstance
    to create the object without security checks.
    """
    cid = str(cid)
    typesTool = getToolByName(container, 'portal_types')
    fti = typesTool.getTypeInfo(type_name)
    if not fti:
        raise ValueError('Invalid type %s' % type_name)

    return fti._constructInstance(container, cid, *args, **kw)


def create(ctype, container, id, *args, **kw):
    """ helper to create old-style folders as their regular type/factory has
        been replaced in plone 4 and isn't available anymore for testing """
    if ctype == 'Folder':
        obj = addNonBTreeFolder(container, id, *args, **kw)
        obj._setPortalTypeName(ctype)
        return obj
    else:
        return _createObjectByType(ctype, container, id, *args, **kw)
