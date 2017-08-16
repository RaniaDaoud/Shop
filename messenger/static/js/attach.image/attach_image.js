// attachez image
$(function () {
 
  $("#sendIMG").on('submit',function () {
    
    var data = new FormData(this);
      

    $.ajax({
      url: '/messages/sendIMG/',
      data: data,
      cache: false,
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
       
      //  $("input[name='attachement']").val('');
      //  $("#attach-frame").attr("src", "");
        $("#box").append(data);
      //  $("input[name='message']").val('');
      //  $("input[name='message']").focus();
        var elem = document.getElementById('box');
        elem.scrollTop = elem.scrollHeight;
      }
    });
    return false;
  });
$(".attach").on('change',function () {
  $("#sendIMG").submit();
    
  });

});
  