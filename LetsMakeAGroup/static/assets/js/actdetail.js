$(window).load(function(){
  var allleft = $(".left");
  var allright = $(".right");
  var length = allleft.length;
  var i;
  for (i = 0; i < length; i++) {
    AdjustColumnsHeight(allleft[i],allright[i]);
  }
  
});

function AdjustColumnsHeight(obj1,obj2){
  var h1 = $(obj1).height();
  var h2 = $(obj2).height();
  var mh = Math.max( h1, h2);
  $(obj1).height(mh);
  $(obj2).height(mh);
}