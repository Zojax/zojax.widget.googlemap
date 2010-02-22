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
import simplejson

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
                                          addressId:'%(addressId)s',
                                          geocodeButtonId:'%(geocodeButtonId)s',
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
    
    @property
    def addressId(self):
        return self.id + '-address'
    
    @property
    def geocodeButtonId(self):
        return self.id + '-geocode-button'

    def render(self):
        component.getUtility(IGoogleMapConfiglet).includeJsSource()
        location = 'false'
        value = self.value
        if value:
            value = component.getMultiAdapter((self.field, self), interfaces.IDataConverter).toFieldValue(self.value).getValue()

        includeInplaceSource(jssource%{
                'id': self.id,
                'mapId': self.mapId,
                'addressId': self.addressId,
                'geocodeButtonId': self.geocodeButtonId,
                'name': self.name,
                'type': 'google.maps.MapTypeId.%s'%self.field.type,
                'klass': self.klass,
                'value': simplejson.dumps(value),
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
        return simplejson.dumps(value.getValue())

    def toFieldValue(self, value):
        if value == u'':
            return self.field.missing_value
        try:
            fvalue = simplejson.loads(value)
            return MapGeocode(fvalue['position']['latitude'],
                              fvalue['position']['longitude'],
                              fvalue['center']['latitude'],
                              fvalue['center']['longitude'],
                              fvalue['zoom'],
                              fvalue['geocode'])
        except (IndexError, TypeError, ValueError), err:
            raise FormatterValidationError(err.args[0], value)
