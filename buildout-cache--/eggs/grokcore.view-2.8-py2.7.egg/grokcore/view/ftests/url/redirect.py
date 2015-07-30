"""
Views have a redirect() method to easily create redirects:

  >>> getRootFolder()['manfred'] = manfred = Mammoth()

Since the index view redirects to mammoth, we expect to see the URL
point to mammoth:

  >>> from zope.app.wsgi.testlayer import Browser, http
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open('http://localhost/manfred')
  >>> browser.url
  'http://localhost/manfred/another'

  >>> response = http('GET /manfred/trustedredirect HTTP/1.0')
  >>> response.getStatus()
  302
  >>> response.getHeader('location')
  'http://www.google.com/ncr'


  >>> browser.open('http://localhost/manfred/redirectwithstatus')
  Traceback (most recent call last):
  ...
  HTTPError: HTTP Error 418: Unknown
  >>> browser.url
  'http://localhost/manfred/redirectwithstatus'

"""
import grokcore.view as grok

class Mammoth(grok.Context):
    pass

class Index(grok.View):
    def render(self):
        self.redirect(self.url('another'))

class TrustedRedirect(grok.View):
    def render(self):
        self.redirect('http://www.google.com/ncr', trusted=True)

class RedirectWithStatus(grok.View):
    def render(self):
        self.redirect(self.url(), status=418)

class Another(grok.View):
    def render(self):
        return "Another view"
