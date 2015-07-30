# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTFolderMixin
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import NextPreviousAwareSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interface import IATBTreeFolder
from Products.ATContentTypes.interface import IATFolder
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.CMFCore.permissions import View
from plone.app.folder import packageName
from plone.app.folder.base import BaseBTreeFolder
from zope.interface import implementer


ATFolderSchema = ATContentTypeSchema.copy() + \
    ConstrainTypesMixinSchema.copy() + NextPreviousAwareSchema.copy()
finalizeATCTSchema(ATFolderSchema, folderish=True, moveDiscussion=False)


class IATUnifiedFolder(IATFolder):
    """ marker interface for the new, unified folders """


@implementer(IATUnifiedFolder, IATBTreeFolder)
class ATFolder(ATCTFolderMixin, BaseBTreeFolder):
    """ a folder suitable for holding a very large number of items """

    schema = ATFolderSchema
    security = ClassSecurityInfo()

    portal_type = 'Folder'
    archetype_name = 'Folder'
    assocMimetypes = ()
    assocFileExt = ()
    cmf_edit_kws = ()

    # Enable marshalling via WebDAV/FTP/ExternalEditor.
    __dav_marshall__ = True

    @security.protected(View)
    def getNextPreviousParentValue(self):
        """ If the parent node is also an IATFolder and has next/previous
            navigation enabled, then let this folder have it enabled by
            default as well """
        parent = self.getParentNode()
        if IATFolder.providedBy(parent):
            return parent.getNextPreviousEnabled()
        else:
            return False


registerATCT(ATFolder, packageName)
