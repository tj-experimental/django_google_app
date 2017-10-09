
const initFusionTable = (map) => {
    const service = new google.maps.places.PlacesService(map);
    const layer = new google.maps.FusionTablesLayer({
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
        let row = e.row;
        let address = row.address.value;
        let computedAddress = row.computed_address.value;
        let longitude = row.longitude.value;
        let latitude = row.latitude.value;

        e.infoWindowHtml = `
        <h3>Searched Address </h3> 
        </br><b>Address: </b>${address}
        </br><b>Computed address: </b> ${computedAddress}
        </br><b>Latitude: </b> ${latitude} 
        </br><b>Longitude: </b> ${longitude}`;
    });
};
