import doctest
import unittest

from zope.interface import implements
from plone.testing import layered
from plone.app.testing.bbb import PTC_FUNCTIONAL_TESTING
from Testing import ZopeTestCase as ztc

import borg.localrole
from borg.localrole import factory_adapter
from borg.localrole import default_adapter


class SimpleLocalRoleProvider(object):
    implements(borg.localrole.interfaces.ILocalRoleProvider)

    def __init__(self, context):
        self.context = context

    def getRoles(self, user):
        """Grant everyone the 'Foo' role"""
        return ('Foo', )

    def getAllRoles(self):
        """In the real world we would enumerate all users and
        grant the 'Foo' role to each, but we won't"""
        yield ('bogus_user', ('Foo', ))


class DummyUser(object):
    def __init__(self, uid, group_ids=()):
        self.id = uid
        self._groups = group_ids

    def getId(self):
        return self.id

    def _check_context(self, obj):
        return True

    def getGroups(self):
        return self._groups

    def getRoles(self):
        return ()


def test_suite():
    suite = [
        layered(doctest.DocFileSuite(
                    'README.txt', package='borg.localrole',
                    optionflags=(doctest.ELLIPSIS |
                                 doctest.NORMALIZE_WHITESPACE)),
                layer=PTC_FUNCTIONAL_TESTING),
    # Add the tests that register adapters at the end
        doctest.DocTestSuite(borg.localrole.workspace,
            setUp=ztc.placeless.setUp(),
            tearDown=ztc.placeless.tearDown(),
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
        doctest.DocTestSuite(factory_adapter),
        doctest.DocTestSuite(default_adapter),
        ]

    return unittest.TestSuite(suite)
