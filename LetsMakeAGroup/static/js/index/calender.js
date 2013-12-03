var calendar_popup;

$(document).ready(function() {
    $('#calendar').fullCalendar({
        // put your options and callbacks here
        events: function(start, end, callback) {
            $.ajax({
                type: "GET",
                url: "get_events",
                success: function(msg){
                    var events = [];
                    //eventlist = [];
                    evenJSON = JSON.parse(msg);
                    var holding = evenJSON['holding'];

                    for(var i=0; i<holding.length; i++) {
                        events.push({
                                     url: "/activitydetail/"+holding[i][0],
                                     title: holding[i][1],
                                     start: holding[i][2],
                                     color: 'CadetBlue'
                        });
                    }

                    var following = evenJSON['following'];
                    for(i=0; i<following.length; i++) {
                        events.push({
                                     url: "/activitydetail/"+following[i][0],
                                     title: following[i][1],
                                     start: following[i][2],
                                     color: 'light blue'
                        });
                    }
                    callback(events);
                },//end success
                error: function(xhr, textStatus, errorThrown) {
                    alert("reload error: "+errorThrown+xhr.status+xhr.responseText);
                }//end error
             });//end of $.ajax
        }//end of events function
    });

    calendar_popup = function () {
        $('#calender_popup').modal('show');
        //markClender();
        setTimeout(today, 150);
    };

    function today() {
        $('#calendar').fullCalendar('today');
    }
});