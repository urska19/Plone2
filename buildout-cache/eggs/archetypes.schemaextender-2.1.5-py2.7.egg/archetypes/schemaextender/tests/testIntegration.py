import doctest
from unittest import TestSuite

from zope.component import testing
from plone.testing import layered
from plone.app.testing.bbb import PTC_FUNCTIONAL_TESTING


def test_suite():
    return TestSuite([
        doctest.DocTestSuite(
            module='archetypes.schemaextender.extender',
            setUp=testing.setUp, tearDown=testing.tearDown),

        layered(doctest.DocFileSuite(
            'usage.txt', package='archetypes.schemaextender',
            ), layer=PTC_FUNCTIONAL_TESTING), ])
