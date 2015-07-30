##############################################################################
#
# Copyright (c) 2006-2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os
import warnings
import re

import zope.component
import grokcore.component
import grokcore.view
from martian.scan import module_info_from_dotted_name
from martian.error import GrokError
from grokcore.view.interfaces import ITemplate, ITemplateFileFactory
from grokcore.view.interfaces import TemplateLookupError
from grokcore.view.components import PageTemplate


class InlineTemplateRegistry(object):
    """Registry managing all inline template files.
    """

    _reg = None
    _unassociated = None

    def __init__(self):
        self.clear()

    def clear(self):
        self._reg = {}
        self._unassociated = set()

    def register_inline_template(self, module_info, template_name, template):
        # verify no file template got registered with the same name
        try:
            existing_template = file_template_registry.lookup(
                module_info, template_name)
        except TemplateLookupError:
            pass
        else:
            template_dir = file_template_registry.get_template_dir(module_info)
            raise GrokError("Conflicting templates found for name '%s': "
                            "the inline template in module '%s' conflicts "
                            "with the file template in directory '%s'" %
                            (template_name, module_info.dotted_name,
                             template_dir), None)

        # register the inline template
        self._reg[(module_info.dotted_name, template_name)] = template
        self._unassociated.add((module_info.dotted_name, template_name))

    def associate(self, module_info, template_name):
        # Two views in the same module should be able to use the same
        # inline template
        try:
            self._unassociated.remove((module_info.dotted_name, template_name))
        except KeyError:
            pass

    def lookup(self, module_info, template_name, mark_as_associated=False):
        result = self._reg.get((module_info.dotted_name, template_name))
        if result is None:
            raise TemplateLookupError(
                "inline template '%s' in '%s' cannot be found" % (
                    template_name, module_info.dotted_name))
        if mark_as_associated:
            self.associate(module_info, template_name)
        return result

    def unassociated(self):
        return self._unassociated


class FileTemplateRegistry(object):
    """Registry managing all template files.
    """

    _reg = None
    _unassociated = None
    _registered_directories = None
    _ignored_patterns = None

    def __init__(self):
        self.clear()

    def clear(self):
        self._reg = {}
        self._unassociated = set()
        self._registered_directories = set()
        self._ignored_patterns = []

    def ignore_templates(self, pattern):
        self._ignored_patterns.append(re.compile(pattern))

    def register_directory(self, module_info):
        # we cannot register a templates dir for a package
        if module_info.isPackage():
            return

        template_dir = self.get_template_dir(module_info)
        # we can only register for directories
        if not os.path.isdir(template_dir):
            return

        # we don't want associated templates become unassociated again
        if template_dir in self._registered_directories:
            return

        for template_file in os.listdir(template_dir):
            template_path = os.path.join(template_dir, template_file)
            self._register_template_file(module_info, template_path)

        self._registered_directories.add(template_dir)

    def _register_template_file(self, module_info, template_path):
        template_dir, template_file = os.path.split(template_path)
        for pattern in self._ignored_patterns:
            if pattern.search(template_file):
                return

        template_name, extension = os.path.splitext(template_file)

        if (template_dir, template_name) in self._reg:
            raise GrokError("Conflicting templates found for name '%s' "
                            "in directory '%s': multiple templates with "
                            "the same name and different extensions." %
                            (template_name, template_dir), None)
        # verify no inline template exists with the same name
        try:
            inline_template_registry.lookup(module_info, template_name)
        except TemplateLookupError:
            pass
        else:
            raise GrokError("Conflicting templates found for name '%s': "
                            "the inline template in module '%s' conflicts "
                            "with the file template in directory '%s'" %
                            (template_name, module_info.dotted_name,
                             template_dir), None)

        extension = extension[1:] # Get rid of the leading dot.

        template_factory = zope.component.queryUtility(
            grokcore.view.interfaces.ITemplateFileFactory,
            name=extension)

        if template_factory is None:
            # Warning when importing files. This should be
            # allowed because people may be using editors that generate
            # '.bak' files and such.
            if extension == 'pt':
                warnings.warn("You forgot to embed the zcml slug for "
                              "grokcore.view. It provides a renderer "
                              "for pt files. Now the file '%s' in '%s' "
                              "cannot be rendered" %
                              (template_file, template_dir), UserWarning, 2)
            else:
                warnings.warn("File '%s' has an unrecognized extension in "
                              "directory '%s'" %
                              (template_file, template_dir), UserWarning, 2)
            return
        template = template_factory(template_file, template_dir)
        template._annotateGrokInfo(template_name, template_path)

        self._reg[(template_dir, template_name)] = template
        self._unassociated.add(template_path)

    def associate(self, template_path):
        # Two views in different module should be able to use the same template
        try:
            self._unassociated.remove(template_path)
        except KeyError:
            pass

    def lookup(self, module_info, template_name, mark_as_associated=False):
        template_dir = self.get_template_dir(module_info)
        result = self._reg.get((template_dir, template_name))
        if result is None:
            raise TemplateLookupError(
                "template '%s' in '%s' cannot be found" % (
                    template_name, template_dir))
        if mark_as_associated:
            registered_template_path = self._reg.get(
                (template_dir, template_name)).__grok_location__
            self.associate(registered_template_path)
        return result

    def unassociated(self):
        return self._unassociated

    def get_template_dir(self, module_info):
        template_dir_name = grokcore.view.templatedir.bind().get(
            module_info.getModule())
        if template_dir_name is None:
            template_dir_name = module_info.name + '_templates'

        template_dir = module_info.getResourcePath(template_dir_name)

        return template_dir

inline_template_registry = InlineTemplateRegistry()
file_template_registry = FileTemplateRegistry()

def register_inline_template(module_info, template_name, template):
    return inline_template_registry.register_inline_template(
        module_info, template_name, template)

def register_directory(module_info):
    return file_template_registry.register_directory(module_info)

def _clear():
    """Remove the registries (for use by tests)."""
    inline_template_registry.clear()
    file_template_registry.clear()

try:
    from zope.testing.cleanup import addCleanUp
except ImportError:
    # don't have that part of Zope
    pass
else:
    addCleanUp(_clear)
    del addCleanUp

def lookup(module_info, template_name, mark_as_associated=False):
    try:
        return file_template_registry.lookup(
            module_info, template_name, mark_as_associated)
    except TemplateLookupError, e:
        try:
            return inline_template_registry.lookup(
                module_info, template_name, mark_as_associated)
        except TemplateLookupError, e2:
            # re-raise first error again
            raise e

def check_unassociated():
    unassociated = inline_template_registry.unassociated()
    if unassociated:
        for dotted_name, template_name in unassociated:
            msg = (
                "Found the following unassociated template "
                "after configuration in  %r: %s." % (
                    dotted_name, template_name))
            warnings.warn(msg, UserWarning, 1)
    unassociated = file_template_registry.unassociated()
    for template_name in unassociated:
        msg = (
            "Found the following unassociated template "
            "after configuration: %s"  % (
                template_name))
        warnings.warn(msg, UserWarning, 1)


def associate_template(module_info, factory, component_name,
                       has_render, has_no_render):
    """Associate a template to a factory located in the module
    described by module_info.
    """
    explicit_template = False
    factory_name = factory.__name__.lower()
    module_name, template_name = grokcore.view.template.bind(
        default=(None, None)).get(factory)
    if template_name is None:
        # We didn't used grok.template. Default the template name to
        # the factory name.
        template_name = factory_name
    else:
        # We used grok.template. Use the same module_info to fetch the
        # template that the module in which the directive have been
        # used (to get the grok.templatedir value).
        assert module_name is not None, \
            u"module_name cannot be None if template_name is specified."
        module_info = module_info_from_dotted_name(module_name)
        explicit_template = True

    # We used grok.template, to specify a template which is different
    # than the class name. Check if there is no template with the same
    # name as the view
    if factory_name != template_name:
        try:
            lookup(module_info, factory_name)
            raise GrokError("Multiple possible templates for %s %r. It "
                            "uses grok.template('%s'), but there is also "
                            "a template called '%s'."
                            % (component_name, factory, template_name,
                               factory_name), factory)
        except TemplateLookupError:
            pass

    # Check if view already have a template set with template =
    factory_have_template = (
        getattr(factory, 'template', None) is not None and
        ITemplate.providedBy(factory.template))

    # Lookup for a template in the registry
    try:
        factory.template = lookup(
            module_info, template_name, mark_as_associated=True)

        # If we associate a template, set the static_name to use to
        # the same package name as where the template is found.
        factory.__static_name__ = module_info.package_dotted_name

        # We now have a template.
        factory_have_template = True
    except TemplateLookupError:
        pass

    if not factory_have_template:
        # If a template was explicitly asked, error.
        if explicit_template:
            raise GrokError(
                "Template %s for %s %r cannot be found." %
                (template_name, component_name.title(), factory), factory)

        # Check for render or error.
        if  has_no_render(factory):
            raise GrokError(
                "%s %r has no associated template or 'render' method." %
                (component_name.title(), factory), factory)

    if has_render(factory):
        # Check for have both render and template
        if factory_have_template:
            raise GrokError(
                "Multiple possible ways to render %s %r. "
                "It has both a 'render' method as well as "
                "an associated template." %
                (component_name, factory), factory)

        # Set static_name to use if no template are found.
        if getattr(factory, '__static_name__', None) is None:
            factory.__static_name__ = module_info.package_dotted_name

    if factory_have_template:
        factory.template._initFactory(factory)


class PageTemplateFileFactory(grokcore.component.GlobalUtility):
    grokcore.component.implements(ITemplateFileFactory)
    grokcore.component.name('pt')

    def __call__(self, filename, _prefix=None):
        return PageTemplate(filename=filename, _prefix=_prefix)


