# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getUtility
from zope.interface import implementer
import logging
import re

logger = logging.getLogger('plone.portlet.static')


class IStaticPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        constraint=re.compile("[^\s]").match,
        required=False)

    text = RichText(
        title=_(u"Text"),
        description=_(u"The text to render"),
        required=True)

    omit_border = schema.Bool(
        title=_(u"Omit portlet border"),
        description=_(
            u"Tick this box if you want to render the text above "
            "without the standard header, border or footer."
        ),
        required=True,
        default=False)

    footer = schema.TextLine(
        title=_(u"Portlet footer"),
        description=_(u"Text to be shown in the footer"),
        required=False)

    more_url = schema.ASCIILine(
        title=_(u"Details link"),
        description=_(
            u"If given, the header and footer will link to this URL."
        ),
        required=False)


@implementer(IStaticPortlet)
class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    header = _(u"title_static_portlet", default=u"Static text portlet")
    text = u""
    omit_border = False
    footer = u""
    more_url = ''

    def __init__(self, header=u"", text=u"", omit_border=False, footer=u"",
                 more_url=''):
        self.header = header
        self.text = text
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave or
        static string if title not defined.
        """
        return self.header or _(u'portlet_static', default=u"Static Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('static.pt')

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        if header:
            normalizer = getUtility(IIDNormalizer)
            return "portlet-static-%s" % normalizer.normalize(header)
        return "portlet-static"

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)

    def transformed(self, mt='text/x-html-safe'):
        """Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.
        """
        orig = self.data.text
        context = aq_inner(self.context)

        if isinstance(orig, RichTextValue):
            orig = orig.raw

        if not isinstance(orig, unicode):
            # Apply a potentially lossy transformation, and hope we stored
            # utf-8 text. There were bugs in earlier versions of this portlet
            # which stored text directly as sent by the browser, which could
            # be any encoding in the world.
            orig = unicode(orig, 'utf-8', 'ignore')
            logger.warn(
                "Static portlet at %s has stored non-unicode text. "
                "Assuming utf-8 encoding." % context.absolute_url()
            )

        # Portal transforms needs encoded strings
        orig = orig.encode('utf-8')

        transformer = getToolByName(context, 'portal_transforms')
        transformer_context = context
        if hasattr(self, '__portlet_metadata__'):
            if ('category' in self.__portlet_metadata__ and
                    self.__portlet_metadata__['category'] == 'context'):
                assignment_context_path = self.__portlet_metadata__['key']
                assignment_context = context.unrestrictedTraverse(assignment_context_path)
                transformer_context = assignment_context
        data = transformer.convertTo(mt, orig,
                                     context=transformer_context, mimetype='text/html')
        result = data.getData()
        if result:
            if isinstance(result, str):
                return unicode(result, 'utf-8')
            return result
        return None


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    schema = IStaticPortlet
    label = _(u"title_add_static_portlet", default=u"Add static text portlet")
    description = _(
        u"description_static_portlet",
        default=u"A portlet which can display static HTML text."
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    schema = IStaticPortlet
    label = _(
        u"title_edit_static_portlet",
        default=u"Edit static text portlet"
    )
    description = _(
        u"description_static_portlet",
        default=u"A portlet which can display static HTML text."
    )
