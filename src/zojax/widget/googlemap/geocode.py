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
from zope import interface, schema
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
        
    def getValue(self):
        return {'position': {'latitude': self.latitude,
                             'longitude': self.longitude,
                             }
               }

class MapGeocode(Geocode):

    interface.implements(IMapGeocode)

    centerLatitude = fieldproperty.FieldProperty(IMapGeocode['centerLatitude'])

    centerLongitude = fieldproperty.FieldProperty(IMapGeocode['centerLongitude'])

    zoom = fieldproperty.FieldProperty(IMapGeocode['zoom'])
    
    geocode = fieldproperty.FieldProperty(IMapGeocode['geocode'])

    def __init__(self, latitude, longitude, centerLatitude, centerLongitude, zoom, geocode):
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.centerLatitude = float(centerLatitude)
        self.centerLongitude = float(centerLongitude)
        self.zoom = zoom
        self.geocode = geocode
        
    def getValue(self):
        res = super(MapGeocode, self).getValue()
        res['center'] = {'latitude': self.centerLatitude,
                         'longitude': self.centerLongitude,
                         }
        res['zoom'] = self.zoom
        res['geocode'] = self.geocode
        return res