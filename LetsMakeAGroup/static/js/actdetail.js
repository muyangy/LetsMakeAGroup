$(window).load(function(){
  var allleft = $(".left");
  var allright = $(".right");
  var length = allleft.length;
  var i;
  for (i = 0; i < length; i++) {
    AdjustColumnsHeight(allleft[i],allright[i]);
  }
    $('#joinpic').click(function(event){
      var actid = $('#actidhidden').text();
      var actuserid = $('#actuseridhidden').text();
      var userid = $('#useridhidden').text();
      var mark = $('#markhidden').text();
      var text = $('#markfollowerhidden').text();
      if(actuserid!=userid && mark =="0" && !text){
        $.ajax({
          type: "GET",
          url: "/join/"+actid,
          success: function(msg){
            $('#markhidden').text("1");
            $('#allfollowers').append("<img src='/infophoto/"+userid+"' style='max-height:50px; max-width:50px;'>");
          }
        });
      }
    });
  
});

function AdjustColumnsHeight(obj1,obj2){
  var h1 = $(obj1).height();
  var h2 = $(obj2).height();
  var mh = Math.max( h1, h2);
  $(obj1).height(mh);
  $(obj2).height(mh);
}