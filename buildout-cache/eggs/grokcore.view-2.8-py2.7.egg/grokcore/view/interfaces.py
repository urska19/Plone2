##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Grok interfaces
"""
from zope.interface import Interface, Attribute
from zope.publisher.interfaces.browser import IBrowserPage, IBrowserView
from zope.contentprovider.interfaces import IContentProvider

class IBaseClasses(Interface):
    View = Attribute("Base class for browser views.")

    ContentProvider = Attribute("Base class for content providers.")

    DirectoryResource = Attribute(
        "Base class to create new directory resource.")


class IDirectives(Interface):

    def layer(layer):
        """Declare the layer for the view.

        This directive acts as a contraint on the 'request' of
        grok.View. This directive can only be used on class level."""

    def path(path):
        """Declare which path to use on a DirectoryResource.

        This directive can only be used on class level."""

    def skin(skin):
        """Declare this layer as a named skin.

        This directive can only be used on class level."""

    def template(template):
        """Declare the template name for a view.

        This directive can only be used on class level."""

    def templatedir(directory):
        """Declare a directory to be searched for templates.

        By default, grok will take the name of the module as the name
        of the directory.  This can be overridden using
        ``templatedir``."""

    def view(view):
        """Define on which view a viewlet manager/viewlet is registered.
        """


class IGrokcoreViewAPI(IBaseClasses, IDirectives):

    def url(request, obj, name=None, data=None):
        """Generate the URL to an object with optional name attached.
        An optional argument 'data' can be a dictionary that is converted
        into a query string appended to the URL."""

    def make_checker(factory, view_factory, permission, method_names=None):
        """Make a checker for a view_factory associated with factory.

        These could be one and the same for normal views, or different
        in case we make method-based views such as for JSON and XMLRPC.
        """

    def PageTemplate(template):
        """Create a Grok PageTemplate object from ``template`` source
        text.  This can be used for inline PageTemplates."""

    def PageTemplateFile(filename):
        """Create a Grok PageTemplate object from a file specified by
        ``filename``.  It will be treated like an inline template
        created with ``PageTemplate``."""

    IBrowserRequest = Attribute('Browser request interface')
    IDefaultBrowserLayer = Attribute('Default layer for browser views.')
    IGrokSecurityView = Attribute('Marker interface for permissive views.')


class IGrokView(IBrowserPage, IBrowserView):
    """Grok views all provide this interface."""

    context = Attribute('context', "Object that the view presents.")

    request = Attribute('request', "Request that the view was looked up with.")

    response = Attribute('response', "Response object that is "
                         "associated with the current request.")

    static = Attribute('static', "Directory resource containing "
                       "the static files of the view's package.")

    def redirect(url):
        """Redirect to given URL"""

    def url(obj=None, name=None, data=None):
        """Construct URL.

        If no arguments given, construct URL to view itself.

        If only obj argument is given, construct URL to obj.

        If only name is given as the first argument, construct URL
        to context/name.

        If both object and name arguments are supplied, construct
        URL to obj/name.

        Optionally pass a 'data' keyword argument which gets added to the URL
        as a cgi query string.
        """

    def default_namespace():
        """Returns a dictionary of namespaces that the template
        implementation expects to always be available.

        This method is *not* intended to be overridden by application
        developers.
        """

    def namespace():
        """Returns a dictionary that is injected in the template
        namespace in addition to the default namespace.

        This method *is* intended to be overridden by the application
        developer.
        """

    def update(**kw):
        """This method is meant to be implemented by grok.View
        subclasses.  It will be called *before* the view's associated
        template is rendered and can be used to pre-compute values
        for the template.

        update() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request)."""

    def render(**kw):
        """A view can either be rendered by an associated template, or
        it can implement this method to render itself from Python.
        This is useful if the view's output isn't XML/HTML but
        something computed in Python (plain text, PDF, etc.)

        render() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request)."""

    def __call__():
        """This is the main method called by Zope to render the
        view. You can use that method if you whish to render the
        view."""


class ITemplateFileFactory(Interface):
    """Utility that generates templates from files in template directories.
    """

    def __call__(filename, _prefix=None):
        """Creates an ITemplate from a file

        _prefix is the directory the file is located in
        """


class ITemplate(Interface):
    """Template objects
    """

    def _initFactory(factory):
        """Template language specific initializations on the view factory."""

    def render(view):
        """Renders the template"""


class TemplateLookupError(Exception):
    pass


class ITemplateRegAPI(Interface):
    """Public API for the templatereg module.
    """
    def register_inline_template(module_info, template_name, template):
        """Register an inline template with the template registry.

        module_info - the module_info of the module the inline template is in
        template_name - the name of the template
        template - the template itself
        """

    def register_directory(module_info):
        """Register a template directory for a module.

        module_info - the module_info of the module
        """

    def lookup(module_info, template_name, mark_as_associated=False):
        """Look up a template for a module.

        module_info - the module info for which to look up the template
        template_name - the name of the template to look up
        mark_as_associated - if a template is found, mark it as associated (disabled by default).
        """


class IGrokSecurityView(Interface):
    """A view treated special by the Grok publisher.

    Views that provide this interface are treated more generously by
    the Grok publisher, as they are allowed to use attributes, which
    are not covered by permission setttings.

    `grok.Permission` and `grok.require` settings however, will be
    applied to such views.
    """


class IContentProvider(IContentProvider):

    context = Attribute(
        'context', "Context object for the content provider.")

    request = Attribute(
        'request', "Request object for the content provider.")

    view = Attribute(
        'view', "View object for the content provider.")

    static = Attribute(
        'static',
        "Directory resource containing the static files of the "
        "content provider's package.")
