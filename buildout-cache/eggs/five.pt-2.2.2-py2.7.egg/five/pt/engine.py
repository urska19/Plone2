"""Patch legacy template classes.

We patch the ``TALInterpreter`` class as well as the cook-method on
the pagetemplate base class (which produces the input for the TAL
interpreter).
"""

import sys

from zope.tal.talinterpreter import TALInterpreter
from zope.interface import implements
from zope.interface import classProvides

from zope.pagetemplate.pagetemplate import PageTemplate
from zope.pagetemplate.interfaces import IPageTemplateEngine
from zope.pagetemplate.interfaces import IPageTemplateProgram

from z3c.pt.pagetemplate import PageTemplate as ChameleonPageTemplate
from z3c.pt.pagetemplate import PageTemplateFile as ChameleonPageTemplateFile

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PageTemplates.Expressions import getEngine
from Products.PageTemplates import ZRPythonExpr

from chameleon.tales import StringExpr
from chameleon.tales import NotExpr
from chameleon.tal import RepeatDict

from z3c.pt.expressions import PythonExpr

from .expressions import PathExpr
from .expressions import TrustedPathExpr
from .expressions import ProviderExpr
from .expressions import NocallExpr
from .expressions import ExistsExpr
from .expressions import UntrustedPythonExpr


# Declare Chameleon's repeat dictionary public
RepeatDict.security = ClassSecurityInfo()
RepeatDict.security.declareObjectPublic()
RepeatDict.__allow_access_to_unprotected_subobjects__ = True

InitializeClass(RepeatDict)


class Program(object):
    implements(IPageTemplateProgram)
    classProvides(IPageTemplateEngine)

    # Zope 2 Page Template expressions
    secure_expression_types = {
        'python': UntrustedPythonExpr,
        'string': StringExpr,
        'not': NotExpr,
        'exists': ExistsExpr,
        'path': PathExpr,
        'provider': ProviderExpr,
        'nocall': NocallExpr,
        }

    # Zope 3 Page Template expressions
    expression_types = {
        'python': PythonExpr,
        'string': StringExpr,
        'not': NotExpr,
        'exists': ExistsExpr,
        'path': TrustedPathExpr,
        'provider': ProviderExpr,
        'nocall': NocallExpr,
        }

    extra_builtins = {
        'modules': ZRPythonExpr._SecureModuleImporter()
        }

    def __init__(self, template):
        self.template = template

    def __call__(self, context, macros, tal=True, **options):
        if tal is False:
            return self.template.body

        # Swap out repeat dictionary for Chameleon implementation
        # and store wrapped dictionary in new variable -- this is
        # in turn used by the secure Python expression
        # implementation whenever a 'repeat' symbol is found
        kwargs = context.vars
        kwargs['wrapped_repeat'] = kwargs['repeat']
        kwargs['repeat'] = RepeatDict(context.repeat_vars)

        return self.template.render(**kwargs)

    @classmethod
    def cook(cls, source_file, text, engine, content_type):
        if engine is getEngine():
            expression_types = cls.secure_expression_types
        else:
            expression_types = cls.expression_types

        # BBB: Support CMFCore's FSPagetemplateFile formatting
        if source_file is not None and source_file.startswith('file:'):
            source_file = source_file[5:]

        template = ChameleonPageTemplate(
            text, filename=source_file, keep_body=True,
            expression_types=expression_types,
            encoding='utf-8', extra_builtins=cls.extra_builtins,
            )

        return cls(template), template.macros
