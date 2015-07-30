import unittest2 as unittest
import doctest

from plone.testing import layered
from collective.elephantvocabulary.testing import VOCAB_LAYER


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'tests.rst',
                package='collective.elephantvocabulary',
                optionflags=doctest.ELLIPSIS,
            ),
            layer=VOCAB_LAYER
        ),
        layered(
            doctest.DocFileSuite(
                'test_terms_from_registry.rst',
                package='collective.elephantvocabulary',
                optionflags=doctest.ELLIPSIS,
            ),
            layer=VOCAB_LAYER,
        ),
    ])
    return suite
