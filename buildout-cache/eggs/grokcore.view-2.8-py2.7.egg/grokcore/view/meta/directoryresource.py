#############################################################################
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
"""Grokkers for resource directories."""

import os

from zope import interface, component
from zope.security.checker import NamesChecker
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

import martian
from martian.error import GrokError

import grokcore.view
from grokcore.view import components

allowed_resource_names = (
    'GET', 'HEAD', 'publishTraverse', 'browserDefault', 'request', '__call__')

allowed_resourcedir_names = allowed_resource_names + ('__getitem__', 'get')


def _get_resource_path(module_info, path):
    resource_path = module_info.getResourcePath(path)
    if os.path.isdir(resource_path):
        static_module = module_info.getSubModuleInfo(path)
        if static_module is not None:
            if static_module.isPackage():
                raise GrokError(
                    "The '%s' resource directory must not "
                    "be a python package." % path, module_info.getModule())
            else:
                raise GrokError(
                    "A package can not contain both a '%s' "
                    "resource directory and a module named "
                    "'%s.py'" % (path, path), module_info.getModule())
    return resource_path


def _register(config, resource_path, name, layer):
    # public checker by default
    checker = NamesChecker(allowed_resourcedir_names)
    resource_factory = components.DirectoryResourceFactory(
        resource_path, checker, name)

    adapts = (layer,)
    provides = interface.Interface
    config.action(
        discriminator=('adapter', adapts, provides, name),
        callable=grokcore.component.provideAdapter,
        args=(resource_factory, adapts, provides, name),
        )
    return True


class DirectoryResourceGrokker(martian.ClassGrokker):
    martian.component(components.DirectoryResource)

    martian.directive(grokcore.view.name, default=None)
    martian.directive(grokcore.view.path)
    martian.directive(grokcore.view.layer, default=IDefaultBrowserLayer)

    def grok(self, name, factory, module_info, **kw):
        # Need to store the module info object on the directory resource
        # class so that it can look up the actual directory.
        factory.module_info = module_info
        return super(DirectoryResourceGrokker, self).grok(
            name, factory, module_info, **kw)

    def execute(self, factory, config, name, path, layer, **kw):
        resource_path = _get_resource_path(factory.module_info, path)
        name = name or factory.module_info.dotted_name
        return _register(config, resource_path, name, layer)
