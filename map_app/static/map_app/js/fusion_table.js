'use strict';

var initFusionTable = function initFusionTable(map) {
    var service = new google.maps.places.PlacesService(map);
    var layer = new google.maps.FusionTablesLayer({
        query: {
            select: "'latitude', 'longitude'",
            from: $.cookie('fusion_table_id')
        },
        map: map,
        styles: [{
            markerOptions: {
                fillColor: '#f31800',
                fillOpacity: 1.0
            }
        }, {
            where: "'latitude' IS NOT NULL",
            markerOptions: {
                fillColor: "#30d454",
                fillOpacity: 1.0
            }
        }]
    });

    google.maps.event.addListener(layer, 'click', function (e) {
        var row = e.row;
        var address = row.address.value;
        var computedAddress = row.computed_address.value;
        var longitude = row.longitude.value;
        var latitude = row.latitude.value;

        e.infoWindowHtml = '\n        <h3>Searched Address </h3> \n        </br><b>Address: </b>' + address + '\n        </br><b>Computed address: </b> ' + computedAddress + '\n        </br><b>Latitude: </b> ' + latitude + ' \n        </br><b>Longitude: </b> ' + longitude;
    });
};
