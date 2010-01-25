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

from interfaces import IGeocode, IMapGeocode


class Geocode(object):
    interface.implements(IGeocode)

    latitude = fieldproperty.FieldProperty(IGeocode['latitude'])

    longitude = fieldproperty.FieldProperty(IGeocode['longitude'])

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def update(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude


class MapGeocode(Geocode):

    interface.implements(IMapGeocode)

    centerLatitude = fieldproperty.FieldProperty(IMapGeocode['centerLatitude'])

    centerLongitude = fieldproperty.FieldProperty(IMapGeocode['centerLongitude'])

    zoom = fieldproperty.FieldProperty(IMapGeocode['zoom'])

    def __init__(self, latitude, longitude, centerLatitude, centerLongitude, zoom):
        self.latitude = latitude
        self.longitude = longitude
        self.centerLatitude = centerLatitude
        self.centerLongitude = centerLongitude
        self.zoom = zoom