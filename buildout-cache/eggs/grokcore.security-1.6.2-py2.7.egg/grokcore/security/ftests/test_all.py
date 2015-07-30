import re
import doctest
import unittest
import grokcore.security

from pkg_resources import resource_listdir
from zope.testing import renormalizing
from zope.app.wsgi.testlayer import BrowserLayer, http

FunctionalLayer = BrowserLayer(grokcore.security)

checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue
        dottedname = 'grokcore.security.ftests.%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname,
            checker=checker,
            extraglobs=dict(
                http=http,
                getRootFolder=FunctionalLayer.getRootFolder),
            optionflags=(
                doctest.ELLIPSIS +
                doctest.NORMALIZE_WHITESPACE +
                doctest.REPORT_NDIFF))
        test.layer = FunctionalLayer
        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in [
        'role'
        ]:
        suite.addTest(suiteFromPackage(name))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
