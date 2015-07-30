from plone.schema import _
from plone.schema.email import Email, IEmail
from plone.schemaeditor.fields import FieldFactory
from zope.interface import Attribute
from zope.schema import URI
from zope.schema.interfaces import IURI


class IURI(IURI):

    # prevent some settings from being included in the field edit form
    default = Attribute('')


class IEmail(IEmail):

    # prevent some settings from being included in the field edit form
    default = Attribute('')


URIFactory = FieldFactory(URI, _(u'URL'))
EmailFactory = FieldFactory(Email, _(u'Email'))
