var zojax = zojax || {};
zojax.googlemap = {
    initializeWidget: function(config){
        /*config is of the form
          {id: "some-dom-element-id",
          mapId: "some-dom-element-id",
          zoom: 12, //the desired zoom level,
          type: G_NORMAL_MAP, //a google maps map type string.
          controls: ['GLargeMapControl'],
          popup_marker: null, // number of the marker with popup or null
          markers: [{latitude: 3.1234,
                     longitude: 4.52342,
                     html: "stuff that appears in the window",
                     popup_on_mode: false}]} //an array of markers.
        */
        config =  $.extend({type: google.maps.MapTypeId.ROADMAP, 
                            mapTypeControl: true,
                            navigationControl: true,
                            scaleControl: true,
                            zoom: 0,
                            value: false,
                            readonly: false,
                            message: ''},
                           config);
        var center = new google.maps.LatLng(0.0, 0.0);
        var options = {mapTypeId: config.type,
                       center: center,
                       zoom: config.zoom,
                       mapTypeControl: config.mapTypeControl,
                       navigationControl: config.navigationControl,
                       scaleControl: config.scaleControl,
                       };
        var map = new google.maps.Map(document.getElementById(config.mapId), options);
        map.setCenter(center);
        map.infowindow = new google.maps.InfoWindow();
        if (config.value) {
            var value = config.value
            map.setCenter(new google.maps.LatLng(value.center.latitude, value.center.longitude));
            map.setZoom(value.zoom);
            var point = new google.maps.LatLng(value.position.latitude, value.position.longitude);
            initMarker(point, config.readonly);
        }
        else {
            if (!config.readonly) {
                var infowindow = new google.maps.InfoWindow({
                    content: config.message,
                    position: map.getCenter()
                    });
                infowindow.open(map);
            }
            var markerListener = google.maps.event.addListener(map, "click", function(event) {
                if (!map.marker) {
                    initMarker(event.latLng, config.readonly)
                }
                else {
                    google.maps.event.removeListener(markerListener);
                }
            })
        };
        var markerUpdateListener = google.maps.event.addListener(map, "bounds_changed", function() {
            if (map.marker) {
                updateMarkerPos(map.marker)
            }
        })

        setTimeout(function () {
            if (map.marker) {
                var bounds = map.getBounds();
                if (!bounds.contains(map.marker.getPosition())) {
                    bounds.extend(map.marker.getPosition());
                    map.fitBounds(bounds);
                }
            }
        }, 2000);
        
        function initMarker(point, readonly)
        {
            var marker = new google.maps.Marker({position: point, draggable: !readonly});
            if (!readonly) {
                google.maps.event.addListener(marker, "position_changed", function() {
                  updateMarkerPos(marker);
                  });
            }
            marker.setMap(map);
            map.marker = marker;
            updateMarkerPos(marker);
            map.infowindow.open(map, marker);
        };

        function updateMarkerPos(marker) {
            if (marker) {
                var coder = new google.maps.Geocoder();
                setTimeout(function () {
                    coder.geocode({'latLng': marker.getPosition()}, function(response, status) {
                        if (status == google.maps.GeocoderStatus.OK) {
                            try {
                                var resp = response[1].address_components;
                                var ind = resp.length;
                                var geocode = {'country': resp[ind-1].short_name,
                                               'state': resp[ind-2].short_name,
                                               'city': resp[ind-3].short_name};
                                document.getElementById(config.id).value = $.toJSON(
                                    {'position': {'latitude': marker.getPosition().lat(),
                                                  'longitude': marker.getPosition().lng()
                                                 },
                                    'center': {'latitude': map.getCenter().lat(),
                                               'longitude': map.getCenter().lng()
                                              },
                                    'zoom': map.getZoom(),
                                    'geocode': geocode});
                                map.infowindow.setContent(response[1].formatted_address);
                            }
                            catch (e) {
                                map.infowindow.setContent("Can't get political location, please move marker");
                            }
                        }
                    }, 2000);
              })
            }
        }
    }
};