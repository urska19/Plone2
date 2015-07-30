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
"""Grokkers for Grokcore Annotation component.
"""
from zope import interface, component

from zope.annotation.interfaces import IAnnotations

import martian
from martian import util

import grokcore.annotation

def default_annotation_provides(factory, module, **data):
    base_interfaces = interface.implementedBy(grokcore.annotation.Annotation)
    factory_interfaces = interface.implementedBy(factory)
    real_interfaces = list(factory_interfaces - base_interfaces)
    util.check_implements_one_from_list(real_interfaces, factory)
    return real_interfaces[0]

def default_annotation_name(factory, module, **data):
    return factory.__module__ + '.' + factory.__name__


class AnnotationGrokker(martian.ClassGrokker):
    """Grokker for components subclassed from `grok.Annotation`.
    """
    martian.component(grokcore.annotation.Annotation)
    martian.directive(grokcore.annotation.context, name='adapter_context')
    martian.directive(grokcore.annotation.provides,
                      get_default=default_annotation_provides)
    martian.directive(grokcore.annotation.name,
                      get_default=default_annotation_name)

    def execute(self, factory, config, adapter_context, provides, name, **kw):
        @component.adapter(adapter_context)
        @interface.implementer(provides)
        def getAnnotation(context):
            annotations = IAnnotations(context)
            try:
                result = annotations[name]
            except KeyError:
                result = factory()
                annotations[name] = result

            if result.__parent__ is None:
                result.__parent__ = context
                result.__name__ = name

            return result

        config.action(
            discriminator=('adapter', adapter_context, provides, ''),
            callable=grokcore.component.provideAdapter,
            args=(getAnnotation,),
            )
        return True


