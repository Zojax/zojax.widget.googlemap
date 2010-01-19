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
        if (config.value) {
            var value = config.value
            map.setCenter(new google.maps.LatLng(value.centerLatitude, value.centerLongitude));
            map.setZoom(value.zoom);
            var point = new google.maps.LatLng(value.latitude, value.longitude);
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
        }, 1000);
        
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
        };

        function updateMarkerPos(marker) {
            if (marker) {
              document.getElementById(config.id).value = marker.getPosition() + ':' + map.getCenter() + ':' + map.getZoom();
            }
        }
    }
};