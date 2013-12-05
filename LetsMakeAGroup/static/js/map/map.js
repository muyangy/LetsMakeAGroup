var map_popup;

$(document).ready(function() {
    var map;
    var markers = [];
    //var addresses = ["4609 Forbes Ave, Pittsburgh", "5000 Forbes Ave, Pittsburgh", "4909 Frew St, Pittsburgh"];
    var markcontents = [];
    var addresses = [];
    var iterator = 0;

    function initialize() {
        //set up mapOption
        var mapOptions = {
            zoom: 14,
            zoomControl: true,
            streetViewControl: false,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(document.getElementById("map-canvas"),mapOptions);//layout the map

        geocoder = new google.maps.Geocoder();

        if(navigator.geolocation) {//If the browser is able to get user's location
            navigator.geolocation.getCurrentPosition(function(position) {
                var pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);//user's location
                map.setCenter(pos);
            }, function() {
              handleNoGeolocation(true);
            });
        } else {
            // Browser doesn't support Geolocation
            handleNoGeolocation(false);
        }
    }

    google.maps.event.addDomListener(window, 'load', initialize);

    map_popup = function() {
        if(markers.length!==0) {//There has already been markers
            clearMarkers();
            iterator = 0;
        }
        $('#small_map_popup').modal('show');
        getActivityAddressFromServer();
        getActivityIntroFromServer();
        setTimeout(resize, 500);
        setTimeout(centerUserLocation, 1000);
        setTimeout(markActivity, 1100);
    };

    function resize() {
        google.maps.event.trigger(map, 'resize');
    }

    function centerUserLocation() {
      if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var pos = new google.maps.LatLng(position.coords.latitude,
                                           position.coords.longitude);
          map.setCenter(pos);
        }, function() {
          handleNoGeolocation(true);
        });
      } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
      }
    }

    function markActivity() {
        geocoder = new google.maps.Geocoder();
        for(var i in addresses) {
            //address = addresses[i];
            setTimeout(function() {addMarker();}, i*500);
            //geocoder.geocode({'address': address}, callback());
        }
    }

    function addMarker() {
        geocoder.geocode({'address': addresses[iterator]}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var marker = new google.maps.Marker({
                    position: results[0].geometry.location,
                    animation: google.maps.Animation.DROP,
                    map: map,
                    url: markcontents[iterator-1]["detaillink"],
                    //title: 'Hello World!'
                });
                introduction = markcontents[iterator-1]["briefintro"];
                var infowindow = new google.maps.InfoWindow({
                     content: introduction
                });
                google.maps.event.addListener(marker, 'mouseover', function() {
                    infowindow.open(map,marker);
                });
                google.maps.event.addListener(marker, 'mouseout', function() {
                    infowindow.close(map,marker);
                });
                google.maps.event.addListener(marker, 'click', function() {
                    window.location.href = this.url;
                });
                markers.push(marker);
            } else {
                console.log("Geocode failed " + status);
            }
        });
        iterator++;
    }

    function clearMarkers() {
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(null);
        }
        markers = [];
    }

    function getActivityAddressFromServer() {
        $.ajax({
            type: "GET",
            url: "getActivitiesAddress",
            success: function(msg){
                addresses = JSON.parse(msg);
            },//end success
        });//end of $.ajax
    }

    function getActivityIntroFromServer() {
        $.ajax({
            type: "GET",
            url: "getActivityIntroduction",
            success: function(msg){
                markcontents = JSON.parse(msg);
            },//end success
        });//end of $.ajax
    }

});


// function(results, status) {
//                 if (status == google.maps.GeocoderStatus.OK) {
//                     if (results[0]) {
//                         //map.setZoom(14);
//                         marker = new google.maps.Marker({
//                             position: results[0].geometry.location,
//                             map: map
//                         });

//                         var infowindow = new google.maps.InfoWindow({
//                             map: map,
//                             position: results[0].geometry.location,
//                             //content: 'Location found using HTML5.'
//                         });
//                         infowindow.setContent(results[0].formatted_address);
//                         infowindow.open(map, marker);
//                     }
//                 } else {
//                   alert("Geocoder failed due to: " + status);
//                 }
//             }