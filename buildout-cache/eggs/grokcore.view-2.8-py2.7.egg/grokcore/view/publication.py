# -*- coding: utf-8 -*-
from zope.security.proxy import removeSecurityProxy
from zope.security.checker import selectChecker
from zope.publisher.interfaces.browser import IBrowserView
from zope.app.publication.browser import BrowserPublication
from zope.app.publication.requestpublicationfactories import BrowserFactory
from grokcore.view import IGrokSecurityView


class ZopePublicationSansProxy(object):
    """Mixin that makes a publisher remove security proxies.

    This mixin overrides three methods from the `IPublication`
    interface (defined in `zope.publisher.interfaces`) to alter their
    security behavior.  The normal Zope machinery wraps a security
    proxy around the application object returned by
    `getApplication()`, and around each of the objects returned as
    `traverseName()` is then called for each URL component.  The
    versions here strip the security proxy off instead, returning the
    bare object (unless the object is a non-Grok view, in which case
    we leave the proxy installed for important security
    reasons).  Non-Grok views however, are handled like Grok views, if
    they provide `grokcore.view.IGrokSecurityView`.

    Finally, when `callObject()` is asked to render
    the view, we quickly re-install a security proxy on the object, make
    sure that the current user is indeed allowed to invoke `__call__()`,
    then pass the bare object to the rendering machinery.

    The result is that, in place of the elaborate series of security
    checks made during the processing of a normal Zope request, Grok
    makes only a single security check: to see if the view can be
    permissibly rendered or not.

    """
    def getApplication(self, request):
        result = super(ZopePublicationSansProxy, self).getApplication(request)
        return removeSecurityProxy(result)

    def traverseName(self, request, ob, name):
        result = super(ZopePublicationSansProxy, self).traverseName(
            request, ob, name)
        bare_result = removeSecurityProxy(result)
        if IBrowserView.providedBy(bare_result):
            if IGrokSecurityView.providedBy(bare_result):
                return bare_result
            else:
                return result
        else:
            return bare_result

    def callObject(self, request, ob):
        checker = selectChecker(ob)
        if checker is not None:
            checker.check(ob, '__call__')
        return super(ZopePublicationSansProxy, self).callObject(request, ob)


class GrokBrowserPublication(ZopePublicationSansProxy, BrowserPublication):
    """Combines `BrowserPublication` with the Grok sans-proxy mixin.

    In addition to the three methods that are overridden by the
    `ZopePublicationSansProxy`, this class overrides a fourth: the
    `getDefaultTraversal()` method, which strips the security proxy from
    the object being returned by the normal method.

    """
    def getDefaultTraversal(self, request, ob):
        obj, path = super(GrokBrowserPublication, self).getDefaultTraversal(
            request, ob)
        return removeSecurityProxy(obj), path


class GrokBrowserFactory(BrowserFactory):
    """Returns the classes Grok uses for browser requests and publication.

    When an instance of this class is called, it returns a 2-element
    tuple containing:

    - The request class that Grok uses for browser requests.
    - The publication class that Grok uses to publish to a browser.

    """
    def __call__(self):
        request, publication = super(GrokBrowserFactory, self).__call__()
        return request, GrokBrowserPublication
