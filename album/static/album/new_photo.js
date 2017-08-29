// attachez image
$(function () {
 
  $("#photo").on('submit',function () {
    
    var data = new FormData(this);
      

    $.ajax({
      url: '/album/new/',
      data: data,
      cache: false,
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
       
        
        $(".items").prepend(data);
        $('.item').show();
        
      }
    });
    return false;
  });
$("#file_input").on('change',function () {
  $("#photo").submit();
    
  });

});
  