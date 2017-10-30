
const initFusionTable = (map) => {
    const service = new google.maps.places.PlacesService(map);
    const layer = new google.maps.FusionTablesLayer({
        query: {
            select: "longitude",
            from: $.cookie('fusion_table_id').split(':')[0]
        },
        map: map,
        styles: window.fusionTableStyle
    });

    google.maps.event.clearListeners(layer, 'click');
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
