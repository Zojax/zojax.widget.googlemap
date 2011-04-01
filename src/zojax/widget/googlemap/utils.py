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
import urllib
import simplejson

class UnknownGeocodeError(Exception):
    """Unknown geocode"""


def reverse_geocode(**kw):
    kw['sensor'] = 'true'
    url = 'http://maps.google.com/maps/api/geocode/json?%s'%urllib.urlencode(kw)
    response = simplejson.load(urllib.urlopen(url))
    if response['status'] != 'OK':
        raise UnknownGeocodeError(response)
    resp = response['results'][0]['address_components'];
    def getComponent(resp, type):
        for i in resp:
            if type in i['types']:
                return i['short_name']
            
    return {'geometry': response['results'][0]['geometry'],
            'geocode':{'country': getComponent(resp, 'country'),
                       'state': getComponent(resp, 'administrative_area_level_1'),
                       'city': getComponent(resp, 'locality')}};
                       
def geocode(address):
    mapsUrl = 'http://maps.google.com/maps/geo?q='
    # This joins the parts of the URL together into one string.
    url = ''.join([mapsUrl,urllib.quote(address),'&output=csv'])
        
    # This retrieves the URL from Google, parses out the longitude and latitude,
    # and then returns them as a string.
    coordinates = urllib.urlopen(url).read().split(',')
    coorText = '%s,%s' % (coordinates[3],coordinates[2])
    return coorText