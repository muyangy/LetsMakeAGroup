var friend_selected;
var validate_form;
var geocoder;
$(document).ready(function() {
    geocoder = new google.maps.Geocoder();
    //redefine upload button
    $("#upload_file").click(function () {
        $("#upload_file_for_activity").trigger('click');
    });

    //redefine type radio
    $("#img_Dine").click(function () {
        $("#radio_Dine").trigger('click');
        clear_select();
        $("#img_Dine")[0].setAttribute("class", "activity_type_selection img-circle");
    });

    $("#img_BBQ").click(function () {
        $("#radio_BBQ").trigger('click');
        clear_select();
        $("#img_BBQ")[0].setAttribute("class", "activity_type_selection img-circle");
    });

    $("#img_Camping").click(function () {
        $("#radio_Camping").trigger('click');
        clear_select();
        $("#img_Camping")[0].setAttribute("class", "activity_type_selection img-circle");
    });

    $("#img_Fishing").click(function () {
        $("#radio_Fishing").trigger('click');
        clear_select();
        $("#img_Fishing")[0].setAttribute("class", "activity_type_selection img-circle");
    });

    $("#img_Golf").click(function () {
        $("#radio_Golf").trigger('click');
        clear_select();
        $("#img_Golf")[0].setAttribute("class", "activity_type_selection img-circle");
    });

    $("#img_Pool").click(function () {
        $("#radio_Pool").trigger('click');
        clear_select();
        $("#img_Pool")[0].setAttribute("class", "activity_type_selection img-circle");
    });

    function clear_select(){
        var selects = $("[id^='img_']");
        for(var i=0; i<selects.length; i++) {
            selects[i].setAttribute("class", "activity_type_selection img-circle img-thumbnail");
        }
    }

    //add new invited friend in new friend list
    friend_selected = function() {
        value = $("#invited_friend_select").val();
        if(value=="-1") {
            return;
        }
        id = value.split("/")[0];
        full_name = value.split("/")[1];

        current_invited = $("input[name^='invited_friend_']");

        for(var i=0; i<current_invited.length;i++) {//IF the friend is already there
            if(current_invited[i].getAttribute("value") == id) {
                return;
            }
        }

        current_invited_num = current_invited.length;
        current_invited_num++;
        new_friend =  "<div class='col-md-3'>";
        new_friend += "<input type='hidden' value='" + id + "' name='invited_friend_" + current_invited_num + "'>";
        new_friend += "<a href='/personalhome/"+ id + "'>@" + full_name + "</a>";
        new_friend += "</div>";

        friend_list = $("#invited_friends");
        friend_list.append(new_friend);
    };

    $("#new_activity_form").submit(function(e){
        var name=$("input[name='name']")[0].value;

        if(name===""){
            $("#name_error").show();
            e.preventDefault();
        } else {
            $("#name_error").hide();
        }

        var address = $("input[name='address1']")[0].value;
        address += $("input[name='address2']")[0].value;
        address += $("input[name='city']")[0].value;

        if(address==="") {
            $("#address_error").show();
            e.preventDefault();
        } else {
            $("#address_error").hide();
        }

        var date = $("input[name='date']")[0].value;
        var time = $("input[name='time']")[0].value;

        if(date==="" || time==="") {
            $("#time_error").show();
            e.preventDefault();
        } else {
            $("#time_error").hide();
        }

        address = $("input[name='address1']")[0].value;
        address += " " + $("input[name='address2']")[0].value;
        address += " " +$("input[name='city']")[0].value;

        //first prevent this form to submit
        var thisform = this;
        e.preventDefault();
        $(thisform).unbind('submit');
        geocoder.geocode({'address': address}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                var lat = results[0].geometry.location.lat();
                var lng = results[0].geometry.location.lng();
                var latinput = document.createElement("input");
                latinput.setAttribute("type", "hidden");
                latinput.setAttribute("name", "lat");
                latinput.setAttribute("value", lat);

                var lnginput = document.createElement("input");
                lnginput.setAttribute("type", "hidden");
                lnginput.setAttribute("name", "lng");
                lnginput.setAttribute("value", lng);

                var form = $("#new_activity_form")[0];
                form.appendChild(latinput);
                form.appendChild(lnginput);
                $(thisform).trigger('submit');//When obtain latlng, submit
            } else {
                console.log("Geocode failed " + status);
            }
        });

    });//end of form.submit

});

