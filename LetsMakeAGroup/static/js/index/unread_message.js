//window.onload = alert("haha");
var deleteItem;
var confirmfriendrequest;
var refusefriend;
var ignore;
$(document).ready(function() {
  //------get unread messages and layout----------//
  function get_unread_message() {
    $.ajax({
        type: "GET",
        url: "get_unread_messages",
        success: function(msg){
            unread_messages = JSON.parse(msg);
            activities = unread_messages['activities'];
            uncomfirmedfriends = unread_messages['uncomfirmedfriends'];
            nearbyActivities = unread_messages['nearbyActivities'];
            if(activities.length > 0 || uncomfirmedfriends.length > 0 || nearbyActivities.length > 0) {//if there is unread message
              $("#unread_message").show();
            } else {
              $("#unread_message").hide();
            }
            var audio = document.getElementById("new_message_audio");

            unread_list = $("#unread_list");
            var i;
            for(i=0; i<activities.length; i++) {
              activity = activities[i];
              activityID = Object.keys(activity)[0];
              var old_activity = $("li[activityID='" + activityID + "']")[0];
              if(old_activity){//if this activity is already there
                continue;
              } else {
                var new_activity = document.createElement("li");
                new_activity.setAttribute("activityID", activityID);
                new_activity.innerHTML = activity_to_html(activity);
                unread_list.append(new_activity);
                unread_list.append('<br>');
                //play notification audio
                audio.play();
              }
            }

            for(i=0; i<uncomfirmedfriends.length; i++) {
              unconfirmedfriend = uncomfirmedfriends[i];
              var old_unconfirmedfriend = $("li[unconfirmedFriendID='" + unconfirmedfriend["unConfirmID"] + "']")[0];
              if(old_unconfirmedfriend){//if this activity is already there
                continue;
              } else {
                var new_confirmfriendmsg = document.createElement("li");
                new_confirmfriendmsg.setAttribute("unconfirmedFriendID", unconfirmedfriend["unConfirmID"]);
                new_confirmfriendmsg.innerHTML = confirmfriend_to_html(unconfirmedfriend);
                unread_list.append(new_confirmfriendmsg);
                unread_list.append('<br>');
                audio.play();
              }
            }

            for(i=0; i<nearbyActivities.length; i++) {
              nearbyActivity = nearbyActivities[i];
              activityID = nearbyActivity[0];
              var old_activity_1 = $("li[activityID='" + activityID + "']")[0];
              if(old_activity_1) {
                continue;
              } else {
                var new_activity_1 = document.createElement("li");
                new_activity_1.setAttribute("activityID", activityID);
                new_activity_1.innerHTML = nearby_to_html(nearbyActivity);
                unread_list.append(new_activity_1);
                unread_list.append('<br>');
                //play notification audio
                audio.play();
              }
            }
        }
    });//end of $.ajax
  }//end of get_unread_message()

  function activity_to_html(activity) {
    activityID = Object.keys(activity)[0];
    activityName = activity[activityID];
    var innerHTML = "<button type='button' class='close' style='float:left' activityID='" + activityID + "' onClick='deleteItem(this)'>&times; &nbsp;</button>You are invited to Join: <a href='activitydetail/" + activityID + "' activityID='" + activityID + "' onClick='deleteItem(this)'>" + activityName + "</a>";
    return innerHTML;
  }

  function confirmfriend_to_html(unconfirmedfriend){
    requestfriendname = unconfirmedfriend["requestfriendname"];
    var innerHTML = "<button type='button' class='close' style='float:left' unconfirmedID='" + unconfirmedfriend["unConfirmID"] + "' onClick='refusefriend(this)'>&times; &nbsp;</button><a href= 'personalhome/"+unconfirmedfriend["requestfriendid"]+"'>"+unconfirmedfriend["requestfriendname"]+"</a> Send you a add friend request &nbsp&nbsp&nbsp<a style = 'cursor: pointer' unconfirmedID='" + unconfirmedfriend["unConfirmID"] + "'onClick='confirmfriend(this)' >Confirm</a>&nbsp&nbsp<a style = 'cursor: pointer' refuseFriendID='" + unconfirmedfriend["unConfirmID"] + "'onClick='refusefriend(this)' >Not Now</a>";
    return innerHTML;
  }

  function nearby_to_html(nearbyActivity) {
    activityID = nearbyActivity[0];
    activityName = nearbyActivity[1];
    var innerHTML = "<li activityID='" + activityID + "'><button type='button' class='close' style='float:left' onClick='ignore(this)' activityID='" + activityID + "'>&times; &nbsp;</button>There is an activity very close to you: <a href='activitydetail/" + activityID + "' activityID='"+ activityID +"' onClick='ignore(this)'>" + activityName + "</a></li><br>";
    return innerHTML;
  }

  get_unread_message();//get once on ready
  window.setInterval(get_unread_message, 2000);
  //------get unread messages and layout----------//

  //------Delete unread message----------//
  deleteItem = function (invoker) {
    var ID = invoker.attributes["activityID"].value;//Get activityID
    $.ajax({
        type: "GET",
        url: "delete_unread_activity/" + ID,
    });//end of $.ajax
    invoker.parentElement.remove();//remove a whole <li>
  };//end of deleteItem
  confirmfriend = function(invoker) {
    var ID = invoker.attributes["unconfirmedID"].value;
    $.ajax({
        type: "GET",
        url: "confirmfriendrequest/" + ID,
    });
    invoker.parentElement.remove();
  };
  refusefriend = function(invoker) {
    var ID = invoker.attributes["refuseFriendID"].value;
    $.ajax({
        type: "GET",
        url: "refusefriend/" + ID,
    });
    invoker.parentElement.remove();
  };
  ignore = function(invoker) {
    var ID = invoker.attributes["activityID"].value;
    $.ajax({
        type: "GET",
        url: "ignore_activity/" + ID,
    });
    invoker.parentElement.remove();
  };
  //------Delete unread message----------//
});
