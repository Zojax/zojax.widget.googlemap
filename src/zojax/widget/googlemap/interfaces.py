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
from zope.schema.interfaces import IObject
from zope.i18nmessageid.message import MessageFactory

from zojax.widget.radio.field import RadioChoice

_ = MessageFactory('zojax.widget.googlemap')


class IGoogleMapConfiglet(interface.Interface):

    enabled = schema.Bool(
        title=_(u"Enabled"),
        default=True,
        required=True,)


class IMapLocation(IObject):
    """ map location field """

    type = RadioChoice(
        title=_(u"Type"),
        description=(u"Map type."),
        required=True,
        vocabulary='zojax.widget.googlemap.mapTypes',
        default=u'ROADMAP',)


class IMapLocationPersistent(IMapLocation):
    """ map location persistent field """


class IMapLocationWidget(interface.Interface):
    """ location widget """


class IGeocode(interface.Interface):
    """A geocode representing a particular location on Earth."""

    latitude = schema.Float(
        title=_(u"Latitude"),
        description=(u"The exact latitude of a place on Earth."),
        required=True)

    longitude = schema.Float(
        title=_(u"Longitude"),
        description=_(u"The exact longitude of a place on Earth."),
        required=True)

    def update(latitude, longitude):
        """Update the latitude and longitude with the given values."""

    def getValue():
        """ get value """


class IMapGeocode(IGeocode):

    centerLatitude = schema.Float(
        title=_(u"Center Latitude"),
        description=(u"The exact latitude of a place on Earth."),
        required=False)

    centerLongitude = schema.Float(
        title=_(u"Center Longitude"),
        description=_(u"The exact longitude of a place on Earth."),
        required=False)

    zoom  = schema.Int(
        title=_(u"Zoom level"),
        description=_(u"Map zoom level."),
        min=0,
        required=False)
    
    geocode = schema.Dict(
        title=_(u"Geocode"),
        description=_(u"Political geocode."),
        required=False)
