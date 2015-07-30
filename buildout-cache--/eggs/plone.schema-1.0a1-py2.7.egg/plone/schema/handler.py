from plone.supermodel.exportimport import BaseHandler
from zope.schema import URI
from plone.schema.email import Email

URIHandler = BaseHandler(URI)
EmailHandler = BaseHandler(Email)
