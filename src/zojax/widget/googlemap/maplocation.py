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
import time
from datetime import date, datetime

from zope import interface, component
from zope.i18n import translate
from zope.schema.interfaces import IDate

from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.converter import FormatterValidationError
from zojax.resourcepackage.library import includeInplaceSource

from interfaces import _, IMapLocation, IMapLocationWidget, IGoogleMapConfiglet
from geocode import MapGeocode

jssource = """<script type="text/javascript">
$(document).ready( function() {
        zojax.googlemap.initializeWidget({id:'%(id)s',
                                          mapId:'%(mapId)s',
                                          readonly: %(readonly)s,
                                          value: %(value)s,
                                          type:%(type)s});
});
</script>"""


class MapLocationWidget(TextWidget):
    interface.implements(IMapLocationWidget)

    klass = 'widget-googlemap-maplocation'

    mapKlass = 'widget-googlemap-maplocation-map'

    mapStyle = ''

    placeMessage = _(u'Place marker')

    @property
    def mapId(self):
        return self.id + '-map'

    def render(self):
        component.getUtility(IGoogleMapConfiglet).includeJsSource()
        location = 'false'
        if self.value:
            value = component.getMultiAdapter((self.field, self), interfaces.IDataConverter).toFieldValue(self.value)
            location = {'latitude': value.latitude,
                        'longitude': value.longitude,
                        'centerLatitude': value.centerLatitude,
                        'centerLongitude': value.centerLongitude,
                        'zoom': value.zoom}

        includeInplaceSource(jssource%{
                'id': self.id,
                'mapId': self.mapId,
                'name': self.name,
                'type': 'google.maps.MapTypeId.%s'%self.field.type,
                'klass': self.klass,
                'value': location,
                'message': translate(self.placeMessage),
                'readonly': str(self.readonly \
                                or self.mode == interfaces.DISPLAY_MODE).lower(),
                }, ('googlemap-widgets',))

        return super(MapLocationWidget, self).render()


@component.adapter(IMapLocation, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def MapLocationFieldWidget(field, request):
    """IFieldWidget factory for MapLocationWidget."""
    return FieldWidget(field, MapLocationWidget(request))


class MapLocationDataConverter(BaseDataConverter):
    component.adapts(IMapLocation, IMapLocationWidget)

    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return u''
        return '(%s, %s):(%s, %s):%s' % (value.latitude, value.longitude, \
                                        value.centerLatitude, value.centerLongitude, \
                                        value.zoom)

    def toFieldValue(self, value):
        if value == u'':
            return self.field.missing_value
        try:
            value = value.replace('(','').replace(')','')
            geocode, center, zoom = map(lambda x: x.strip(), value.strip().split(':'))
            lat, lon = map(lambda x: float(x.strip()), geocode.strip().split(','))
            centerLat, centerLon = map(lambda x: float(x.strip()), center.strip().split(','))
            zoom = int(zoom)
            return MapGeocode(lat, lon, centerLat, centerLon, zoom)
        except (IndexError, TypeError, ValueError), err:
            raise FormatterValidationError(err.args[0], value)
