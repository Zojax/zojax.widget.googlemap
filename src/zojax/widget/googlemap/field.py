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
from zope import interface
from zope.schema import Object, fieldproperty

from interfaces import IMapLocation, IMapGeocode


class MapLocation(Object):
    interface.implements(IMapLocation)

    type = fieldproperty.FieldProperty(IMapLocation['type'])

    def __init__(self, *kv, **kw):
        super(MapLocation, self).__init__(IMapGeocode, *kv, **kw)
