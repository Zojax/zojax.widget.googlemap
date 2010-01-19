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
from zope.schema.interfaces import IDate

from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.converter import FormatterValidationError
from zojax.resourcepackage.library import includeInplaceSource, includes

mapsource = """<script type="text/javascript"
src="http://maps.google.com/maps/api/js?sensor=true">
</script>
<script type="text/javascript">
$(document).unload( function() {GUnload();} );
</script>
"""


class GoogleMapConfiglet(object):

    def includeJsSource(self):
        if not self.enabled:
            return
        source = mapsource%{
                }
        if source not in includes.sources:
            includeInplaceSource(source)
