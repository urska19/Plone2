import re
import unittest
import os.path
import grokcore.view

from pkg_resources import resource_listdir

from zope.app.wsgi.testlayer import BrowserLayer, http
from zope.testing import doctest, renormalizing


FunctionalLayer = BrowserLayer(grokcore.view)

checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    getRootFolder = FunctionalLayer.getRootFolder
    globs = dict(http=http,
                 getRootFolder=getRootFolder)
    optionflags = (doctest.ELLIPSIS+
                   doctest.NORMALIZE_WHITESPACE+
                   doctest.REPORT_NDIFF)

    for filename in files:
        if filename == '__init__.py':
            continue

        test = None
        if filename.endswith('.py'):
            dottedname = 'grokcore.view.ftests.%s.%s' % (name, filename[:-3])
            test = doctest.DocTestSuite(
                dottedname,
                checker=checker,
                extraglobs=globs,
                optionflags=optionflags)
            test.layer = FunctionalLayer
        elif filename.endswith('.txt'):
            test = doctest.DocFileSuite(
                os.path.join(name, filename),
                optionflags=optionflags,
                globs=globs)
            test.layer = FunctionalLayer
        if test is not None:
            suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in [
        'contentprovider',
        'directoryresource',
        'static',
        'url',
        'view',
        ]:
        suite.addTest(suiteFromPackage(name))
    return suite
