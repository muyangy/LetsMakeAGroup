$(document).ready(function() {
    /*$('#smallmap').css({
        'position':'fixed',
        'right':'5px',
        'top':'100px',
        'cursor':'pointer',
        'z-index':1
    });*/

   /* $('#new_activity').css({
        'position':'fixed',
        'right':'10px',
        'top':'515px',
        'cursor':'pointer',
        'z-index':1
    });*/

    //redefine upload button
    $("#upload_file").click(function () {
        $("#upload_file_for_activity").trigger('click');
    });

    $("#img_Dine").click(function () {
        $("#radio_Dine").trigger('click');
    });

    $("#img_BBQ").click(function () {
        $("#radio_BBQ").trigger('click');
    });

    $("#img_Camping").click(function () {
        $("#radio_Camping").trigger('click');
    });

    $("#img_Fishing").click(function () {
        $("#radio_Fishing").trigger('click');
    });

    $("#img_Golf").click(function () {
        $("#radio_Golf").trigger('click');
    });

    $("#img_Pool").click(function () {
        $("#radio_Pool").trigger('click');
    });

    //$('#small_map_popup').onshow(function(){
        //initialize();
      //  google.maps.event.trigger(map, 'resize');
    //});

      //function resize() {
        //  $('#small_map_popup').show();
          //google.maps.event.trigger(map, 'resize');
      //}

});


  /* $(window).scroll(function(){
    $('#test').css({
        'position':'fixed',
        'top':'100px',
        'z-index':1
    });
});*/
