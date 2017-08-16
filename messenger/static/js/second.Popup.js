  
$('.btn').on('show', function() {
	$('#myModal1').show();
    $('#myModal1').css('opacity', .5);
    $('#myModal1').unbind();
});
$('.btn').on('hidden', function() {
	$('#myModal1').hide();
    $('#myModal1').css('opacity', 1);
    $('#myModal1').removeData("modal").modal({});
});

