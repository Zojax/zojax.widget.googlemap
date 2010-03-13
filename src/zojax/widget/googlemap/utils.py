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


def geocode(**kw):
    kw['sensor'] = 'true'
    url = 'http://maps.google.com/maps/api/geocode/json?%s'%urllib.urlencode(kw)
    response = simplejson.load(urllib.urlopen(url))
    if response['status'] != 'OK':
        raise UnknownGeocodeError(response)
    resp = response['results'][0]['address_components'];
    ind = len(resp);
    return {'geometry': response['results'][0]['geometry'],
            'geocode':{'country': resp[ind-1]['short_name'],
                       'state': resp[ind-2]['short_name'],
                       'city': resp[ind-3]['short_name']}};