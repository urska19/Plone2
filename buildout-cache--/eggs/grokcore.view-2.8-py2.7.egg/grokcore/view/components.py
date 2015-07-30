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
"""Grok components"""

import sys
import os
import warnings
import fnmatch

from zope import component
from zope import interface
from zope.browserresource import directory
from zope.browserresource.interfaces import IResourceFactoryFactory
from zope.contentprovider.provider import ContentProviderBase
from zope.pagetemplate import pagetemplate, pagetemplatefile
from zope.pagetemplate.engine import TrustedAppPT
from zope.ptresource.ptresource import PageTemplateResourceFactory
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces import NotFound
from zope.publisher.publish import mapply

import martian.util
from grokcore.view import interfaces, util


class ViewSupport(object):
    """Mixin class providing methods and properties generally
    useful for view-ish components.
    """

    @property
    def response(self):
        """The HTTP Response object that is associated with the request.

        This is also available as self.request.response, but the
        response attribute is provided as a convenience.
        """
        return self.request.response

    @property
    def body(self):
        """The text of the request body.
        """
        return self.request.bodyStream.getCacheStream().read()

    def redirect(self, url, status=None, trusted=False):
        """Redirect to `url`.

        The headers of the :attr:`response` are modified so that the
        calling browser gets a redirect status code. Please note, that
        this method returns before actually sending the response to
        the browser.

        `url` is a string that can contain anything that makes sense
        to a browser. Also relative URIs are allowed.

        `status` is a number representing the HTTP status code sent
        back. If not given or ``None``, ``302`` or ``303`` will be
        sent, depending on the HTTP protocol version in use (HTTP/1.0
        or HTTP/1.1).

        `trusted` is a boolean telling whether we're allowed to
        redirect to 'external' hosts. Normally redirects to other
        hosts than the one the request was sent to are forbidden and
        will raise a :exc:`ValueError`.
        """
        return self.request.response.redirect(
            url, status=status, trusted=trusted)

    def url(self, obj=None, name=None, skin=util.ASIS, data=None):
        """Return string for the URL based on the obj and name.

        If no arguments given, construct URL to view itself.

        If only `obj` argument is given, construct URL to `obj`.

        If only name is given as the first argument, construct URL to
        `context/name`.

        If both object and name arguments are supplied, construct URL
        to `obj/name`.

        Optionally pass a `skin` keyword argument. This should be a
        skin component and the skin's name is taken from this
        component. The effect of this argument is a leading
        ``++skin++[skinname]/`` segment in the path-part of the URL.
        When the argument is not passed, whatever skin is currently set
        on the request will be effective in the URL.

        When passing ``None`` whatever skin is currently effective will
        be removed from the URLs.

        Optionally pass a `data` keyword argument which gets added to
        the URL as a CGI query string.

        """
        if isinstance(obj, basestring):
            if name is not None:
                raise TypeError(
                    'url() takes either obj argument, obj, string arguments, '
                    'or string argument')
            name = obj
            obj = None

        if name is None and obj is None:
            # create URL to view itself
            obj = self
        elif name is not None and obj is None:
            # create URL to view on context
            obj = self.context

        return util.url(self.request, obj, name, skin, data)


class View(ViewSupport, BrowserPage):
    interface.implements(interfaces.IGrokView)

    def __init__(self, context, request):
        super(View, self).__init__(context, request)
        self.__name__ = getattr(self, '__view_name__', None)
        static_name = getattr(self, '__static_name__', None)
        if static_name is not None:
            self.static = component.queryAdapter(
                self.request,
                interface.Interface,
                name=static_name)
        else:
            self.static = None

    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue rendering the template or doing anything else.
            return

        template = getattr(self, 'template', None)
        if template is not None:
            return self._render_template()
        return mapply(self.render, (), self.request)

    def _render_template(self):
        return self.template.render(self)

    def default_namespace(self):
        """Returns a dictionary of namespaces that the template implementation
        expects to always be available.

        This method is **not** intended to be overridden by
        application developers.
        """
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['static'] = self.static
        namespace['view'] = self
        return namespace

    def namespace(self):
        """Returns a dictionary that is injected in the template namespace in
        addition to the default namespace.

        This method **is** intended to be overridden by the application
        developer.
        """
        return {}

    def __getitem__(self, key):
        # This is BBB code for Zope page templates only:
        if not isinstance(self.template, PageTemplate):
            raise AttributeError("View has no item %s" % key)

        value = self.template._template.macros[key]
        # When this deprecation is done with, this whole __getitem__ can
        # be removed.
        warnings.warn("Calling macros directly on the view is deprecated. "
                      "Please use context/@@viewname/macros/macroname\n"
                      "View %r, macro %s" % (self, key),
                      DeprecationWarning, 1)
        return value

    def update(self, **kwargs):
        """This method is meant to be implemented by subclasses. It
        will be called before the view's associated template is
        rendered and can be used to pre-compute values for the
        template.

        update() accepts arbitrary keyword parameters which will be
        filled in from the request (in that case they **must** be
        present in the request).
        """
        pass

    def render(self, **kwargs):
        """A view can either be rendered by an associated template, or
        it can implement this method to render itself from Python.
        This is useful if the view's output isn't XML/HTML but
        something computed in Python (plain text, PDF, etc.)

        render() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request).
        """
        pass

    render.base_method = True

# backwards compatibility. Probably not needed by many, but just in case.
# please start using grokcore.view.View again.
CodeView = View


class BaseTemplate(object):
    """Any sort of page template"""

    interface.implements(interfaces.ITemplate)

    __grok_name__ = ''
    __grok_location__ = ''

    def __repr__(self):
        return '<%s template in %s>' % (self.__grok_name__,
                                        self.__grok_location__)

    def _annotateGrokInfo(self, name, location):
        self.__grok_name__ = name
        self.__grok_location__ = location

    def _initFactory(self, factory):
        pass

class ContentProvider(ContentProviderBase):
    interface.implements(interfaces.IContentProvider)

    template = None

    def __init__(self, context, request, view):
        super(ContentProvider, self).__init__(context, request, view)
        self.context = context
        self.request = request
        self.view = view
        self.__name__ = self.__view_name__
        self.static = component.queryAdapter(
            self.request,
            interface.Interface,
            name=self.module_info.package_dotted_name,
            )

    def default_namespace(self):
        namespace = {}
        namespace['context'] = self.context
        namespace['provider'] = self
        namespace['request'] = self.request
        namespace['static'] = self.static
        namespace['view'] = self.view
        return namespace

    def namespace(self):
        return {}

    def _render_template(self):
        return self.template.render(self)

    def render(self, **kwargs):
        """A content provider can either be rendered by an associated
        template, or it can implement this method to render itself from
        Python.  This is useful if the view's output isn't XML/HTML but
        something computed in Python (plain text, PDF, etc.)

        render() can take arbitrary keyword parameters which will be
        filled in from the request (in that case they *must* be
        present in the request).
        """
        return self._render_template()

    render.base_method = True


class GrokTemplate(BaseTemplate):
    """A slightly more advanced page template

    This provides most of what a page template needs and is a good base for
    writing your own page template"""

    def __init__(self, string=None, filename=None, _prefix=None):

        # __grok_module__ is needed to make defined_locally() return True for
        # inline templates
        # XXX unfortunately using caller_module means that care must be taken
        # when GrokTemplate is subclassed. You can not do a super().__init__
        # for example.
        self.__grok_module__ = martian.util.caller_module()

        if not (string is None) ^ (filename is None):
            raise AssertionError(
                "You must pass in template or filename, but not both.")

        if string:
            self.setFromString(string)
        else:
            if _prefix is None:
                module = sys.modules[self.__grok_module__]
                _prefix = os.path.dirname(module.__file__)
            self.setFromFilename(filename, _prefix)

    def __repr__(self):
        return '<%s template in %s>' % (self.__grok_name__,
                                        self.__grok_location__)

    def _annotateGrokInfo(self, name, location):
        self.__grok_name__ = name
        self.__grok_location__ = location

    def _initFactory(self, factory):
        pass

    def namespace(self, view):
        # By default use the namespaces that are defined as the
        # default by the view implementation.
        return view.default_namespace()

    def getNamespace(self, view):
        namespace = self.namespace(view)
        namespace.update(view.namespace())
        return namespace


class TrustedPageTemplate(TrustedAppPT, pagetemplate.PageTemplate):
    pass


class TrustedFilePageTemplate(TrustedAppPT, pagetemplatefile.PageTemplateFile):
    pass


class PageTemplate(GrokTemplate):

    def setFromString(self, string):
        zpt = TrustedPageTemplate()
        if martian.util.not_unicode_or_ascii(string):
            raise ValueError("Invalid page template. Page templates must be "
                             "unicode or ASCII.")
        zpt.write(string)
        self._template = zpt

    def setFromFilename(self, filename, _prefix=None):
        self._template = TrustedFilePageTemplate(filename, _prefix)

    def _initFactory(self, factory):

        def _get_macros(self):
            return self.template._template.macros
        # _template.macros is a property that does template reloading in debug
        # mode.  A direct "factory.macros = macros" basically caches the
        # template.  So we use a property.
        factory.macros = property(_get_macros)

    def render(self, view):
        namespace = self.getNamespace(view)
        template = self._template
        namespace.update(template.pt_getContext())
        return template.pt_render(namespace)


class PageTemplateFile(PageTemplate):
    # For BBB

    def __init__(self, filename, _prefix=None):
        self.__grok_module__ = martian.util.caller_module()
        if _prefix is None:
            module = sys.modules[self.__grok_module__]
            _prefix = os.path.dirname(module.__file__)
        self.setFromFilename(filename, _prefix)


_marker = object()


class DirectoryResource(directory.DirectoryResource):
    forbidden_names = ('.svn', )

    def get(self, name, default=_marker):

        for pat in self.forbidden_names:
            if fnmatch.fnmatch(name, pat):
                if default is _marker:
                    raise NotFound(None, name)
                else:
                    return default

        path = self.context.path
        filename = os.path.join(path, name)
        isfile = os.path.isfile(filename)
        isdir = os.path.isdir(filename)

        if not (isfile or isdir):
            if default is _marker:
                raise NotFound(None, name)
            return default

        if isfile:
            ext = os.path.splitext(os.path.normcase(name))[1][1:]
            factory = component.queryUtility(IResourceFactoryFactory, ext,
                                             self.default_factory)
            if factory is PageTemplateResourceFactory:
                factory = self.default_factory
        else:
            factory = self.directory_factory

        rname = self.__name__ + '/' + name
        resource = factory(filename, self.context.checker, rname)(self.request)
        resource.__parent__ = self
        return resource


class DirectoryResourceFactory(directory.DirectoryResourceFactory):
    # We need this to allow hooking up our own DirectoryResource class.
    factoryClass = DirectoryResource


DirectoryResource.directory_factory = DirectoryResourceFactory
