# -*- coding: utf-8 -*-
"""
There is a url function that can be imported from grok to determine the
absolute URL of objects.

  >>> from grokcore.view import url

  >>> from zope.site.folder import Folder
  >>> herd = Folder()
  >>> getRootFolder()['herd'] = herd
  >>> manfred = Mammoth()
  >>> herd['manfred'] = manfred

Now let's use url on some things::

  >>> from zope.app.wsgi.testlayer import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False
  >>> browser.open("http://localhost/herd/manfred/index")
  >>> print browser.contents
  http://localhost/herd/manfred/index
  >>> browser.open("http://localhost/herd/manfred/another")
  >>> print browser.contents
  http://localhost/herd/manfred/another

We get the views manually so we can do a greater variety of url() calls:

  >>> from zope import component
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> index_view = component.getMultiAdapter((manfred, request), name='index')
  >>> url(request, index_view)
  'http://127.0.0.1/herd/manfred/index'
  >>> another_view = component.getMultiAdapter((manfred, request),
  ...                                              name='another')
  >>> url(request, another_view)
  'http://127.0.0.1/herd/manfred/another'

Now let's get a URL for a specific object:

  >>> url(request, manfred)
  'http://127.0.0.1/herd/manfred'

We can get the URL for any object in content-space:

  >>> url(request, herd)
  'http://127.0.0.1/herd'

We can also pass a name along with this, to generate a URL to a
particular view on the object:

  >>> url(request, herd, 'something')
  'http://127.0.0.1/herd/something'

It works properly in the face of non-ascii characters in URLs:

  >>> u = url(request, herd, unicode('árgh', 'UTF-8'))
  >>> u
  'http://127.0.0.1/herd/%C3%A1rgh'
  >>> import urllib
  >>> expected = unicode('http://127.0.0.1/herd/árgh', 'UTF-8')
  >>> urllib.unquote(u).decode('utf-8') == expected
  True

The url() function supports a data argument which is converted to a
CGI type query string. If any of the values are of type unicode it's
converted to a string assuming the encoding is UTF-8:

  >>> url(request, herd, '@@sample_view', data=dict(age=28))
  'http://127.0.0.1/herd/@@sample_view?age=28'
  
  >>> url(request, herd, data=dict(age=28))
  'http://127.0.0.1/herd?age=28'
  
There is no problem putting one of the 'reserved' arguments inside the data
argument or explicitely supplying 'None':

  >>> url(request, herd, None, data=dict(name="Peter"))
  'http://127.0.0.1/herd?name=Peter'

Providing an empty dict gives the same result than giving None:

  >>> url(request, herd, data={})
  'http://127.0.0.1/herd'

  >>> url(request, herd, data=None)
  'http://127.0.0.1/herd'

Since order in dictionairies is arbitrary we'll test the presence of multiple
keywords by using find()

  >>> withquery = url(request, herd, 'sample_view', data=dict(a=1, b=2, c=3))
  >>> withquery.find('a=1') > -1
  True
  
  >>> withquery.find('b=2') > -1
  True
  
  >>> withquery.find('c=3') > -1
  True

  >>> url(request, herd, 'bar', data='baz')
  Traceback (most recent call last):
    ...
  TypeError: url() data argument must be a dict.

"""
import grokcore.view as grok
from grokcore.view import url
from zope.container.contained import Contained

class Mammoth(Contained):
    pass

grok.context(Mammoth)

class Index(grok.View):
    def render(self):
        return url(self.request, self)

class Another(grok.View):
    def render(self):
        return url(self.request, self)
