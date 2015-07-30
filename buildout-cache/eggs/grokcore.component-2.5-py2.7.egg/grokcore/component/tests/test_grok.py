import re
import unittest
import traceback
import doctest
from pkg_resources import resource_listdir
from zope.testing import cleanup, renormalizing
import zope.component.eventtesting

def setUpZope(test):
    zope.component.eventtesting.setUp(test)

def cleanUpZope(test):
    cleanup.cleanUp()

checker = renormalizing.RENormalizing([
    # str(Exception) has changed from Python 2.4 to 2.5 (due to
    # Exception now being a new-style class).  This changes the way
    # exceptions appear in traceback printouts.
    (re.compile(r"ConfigurationExecutionError: <class '([\w.]+)'>:"),
                r'ConfigurationExecutionError: \1:'),
    ])

def suiteFromPackage(name):
    files = resource_listdir(__name__, name)
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename.endswith('_fixture.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = 'grokcore.component.tests.%s.%s' % (name, filename[:-3])
        try:
            test = doctest.DocTestSuite(dottedname,
                                        setUp=setUpZope,
                                        tearDown=cleanUpZope,
                                        checker=checker,
                                        optionflags=doctest.ELLIPSIS+
                                        doctest.NORMALIZE_WHITESPACE)
        except ImportError:  # or should this accept anything?
            traceback.print_exc()
            raise
        suite.addTest(test)
    return suite

def test_suite():
    suite = unittest.TestSuite()
    for name in ['adapter', 'directive', 'grokker', 'utility', 'view',
                 'event', 'inherit', 'order', 'subscriptions']:
        suite.addTest(suiteFromPackage(name))

    api = doctest.DocFileSuite('api.txt')
    suite.addTest(api)

    # this test cannot follow the normal testing pattern, as the
    # bug it tests for is only exposed in the context of a doctest
    grok_component = doctest.DocFileSuite('grok_component.txt',
                                          setUp=setUpZope,
                                          tearDown=cleanUpZope)
    suite.addTest(grok_component)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
