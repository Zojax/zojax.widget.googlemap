##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""

$Id$
"""
from zope import interface, schema, component

from zojax.content.type.interfaces import IContentTypeChecker, IContentContainer
from zojax.persistent.fields.field import Field
from zojax.persistent.fields.fieldtype import DataProperty

import field, interfaces


class FieldType(type):

    def __new__(cls, name, field, schema, ignoreFields=(), *args, **kw):
        bases = (Field, field)

        cdict = {'__module__': 'zojax.widget.googlemap.persistentfield',
                 'description': schema.__doc__}

        if ignoreFields:
            cdict['ignoreFields'] = ignoreFields

        tp = type.__new__(cls, str(name), bases, cdict)
        interface.classImplements(tp, schema)
        return tp

    def __init__(cls, name, field, schema, *args, **kw):
        cls.__schema__ = DataProperty(schema)


MapLocation = FieldType(
    'MapLocation', field.MapLocation, interfaces.IMapLocationPersistent)



class MapLocationChecker(object):
    interface.implements(IContentTypeChecker)
    component.adapts(MapLocation, IContentContainer)

    def __init__(self, contenttype, context):
        self.contenttype = contenttype
        self.context = context

    def check(self):
        return component.getUtility(interfaces.IGoogleMapConfiglet).enabled
