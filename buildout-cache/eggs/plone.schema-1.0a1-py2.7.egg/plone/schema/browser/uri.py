from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IURI

from plone.app.z3cform.interfaces import IPloneFormLayer


class IURIWidget(ITextWidget):
    """ URI Widget """


@implementer(IURIWidget)
class URIWidget(TextWidget):
    klass = u'uri-widget'
    value = None


@adapter(IURI, IPloneFormLayer)
@implementer(IFieldWidget)
def URIFieldWidget(field, request):
    return FieldWidget(field, URIWidget(request))
