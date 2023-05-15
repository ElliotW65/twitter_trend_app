$(document).ready(function() {
    // Initialise the socket connection to allow for
    // two way communication with the server.
    var socket = io();
    
    // Set container for map
    var mapContainer = document.getElementById('map');
    
    mapboxgl.accessToken = 'pk.eyJ1IjoiZWxsaW90dzY1IiwiYSI6ImNrbGk0amV4MTA5bHUycW5tN2JzM3J0bTIifQ.OGT4ltSNZ7vyd_yEUg8afQ';
    

    // Create map and put in container specified by
    // mapContainer variable.
    var map = new mapboxgl.Map({
        container: mapContainer, // container ID
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [-74.5, 40], // starting position [lng, lat]
        zoom: 9 // starting zoom
    });
    
    // Create marker, enable it to have a popup on
    // click and add it to the map.
    var marker = new mapboxgl.Marker({
        draggable: true,
        color: "#47A7E6"
        })
        .setLngLat([-74.5, 40])
        .setPopup(new mapboxgl.Popup({
            className: "tpopup",
            anchor: 'bottom-left',   // To show popup on top
            //offset: { 'bottom': [20, -20]}
        }).setHTML('Loading...')).addTo(map);
    
    // If the marker is clicked, the coordinates are sent to the
    // server as inputs for the python script that will retrieve
    // and process the data.
    marker.getElement().addEventListener('click', () => {
        sendCoords(marker, socket);
    });
    
    // Event handler receives the data sent from the server,
    // and calls the showTags funciton to process the data and
    // put it in the popup.
    socket.on('data', (data) => {
        showTags(data);
    });
    
    // Create grocoder which enables user to search
    // the map.
    var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl
    });
    
    // Adds a marker to the map in the centre of where the
    // the user searched for.
    geocoder.on('result', function(e) {
        console.log('Called')
        console.log(e.result.center)
        geocoder.clear();
        var marker = new mapboxgl.Marker({ 
            draggable: true, 
            color: "#47A7E6" })
          .setLngLat(e.result.center)
          .setPopup(new mapboxgl.Popup({
            className: "tpopup",
            anchor: 'bottom-left',   // To show popup on top
        })
        .setHTML('Loading...'))
        .addTo(map)

        // When user clicks on the marker the coordinates are sent to
        // the server.
        marker.getElement().addEventListener('click', () => {
            sendCoords(marker, socket);
            console.log('Clicked');
        }); 
    
        // Event handler receives the data sent from the server,
        // and calls the showTags funciton to process the data and
        // put it in the popup.
        socket.on('data', (data) => {
            showTags(data);
        });
      });
    
    // Add geocoder search functionlaity to map
    document.getElementById('geocoder').appendChild(geocoder.onAdd(map));
    
    // Function sends coordinates from a marker to the server.
    function sendCoords(marker, socket) {
        socket.emit('location', marker.getLngLat());
    }

    // Function takes in as a parameter twitter data received
    // received from the server, formats it and puts it in the popup.
    function showTags(data) {
        var str = "<h2 style=\"text-align: centre\">Top 5 Trends</h2> <pre>1. " + data[0].tag
        + "<br>2. "  + data[1].tag
        + "<br>3. "  + data[2].tag
        + "<br>4. "  + data[3].tag
        + "<br>5. "  + data[4].tag + "</pre>"
        document.getElementsByClassName('mapboxgl-popup-content')[0].innerHTML = str;
    }
    
});



