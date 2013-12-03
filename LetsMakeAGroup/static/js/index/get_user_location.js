var calendar_popup;

$(document).ready(function() {
    function get_current_location() {
      if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          $.ajax({
            type: "GET",
            url: "/update_user_location",
            data: {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            },
          });//end of ajax
        }, function() {
          handleNoGeolocation(true);
        });
      } else {
        // Browser doesn't support Geolocation
        handleNoGeolocation(false);
      }
    }
    get_current_location();
});