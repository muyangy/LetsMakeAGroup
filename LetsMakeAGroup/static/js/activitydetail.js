$(document).ready(function() {
	$('#joinpic')[0].click(function(){
        var id = $('#useridhidden')[0].innerhtml;
        $('#allfollowers')[0].append("<img src='/infophoto/"+id+"style='max-height:50px; max-width:50px;'>");

    });
});