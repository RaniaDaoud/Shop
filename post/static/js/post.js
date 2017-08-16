// attachez image
$(function () { 
 
  $("#post").on('submit',function (e) {
    e.preventDefault();
    
    var data = new FormData(this);
      

    $.ajax({
      url: '/post/one/',
      data: data,
      cache: false,
      type: 'POST',
      contentType: false,
      processData: false,
      success: function (data) {
       
      //  $("input[name='attachement']").val('');
      //  $("#attach-frame").attr("src", "");
        $(".box").prepend(data);
      //  $("input[name='message']").val('');
      //  $("input[name='message']").focus();
      /*  var elem = document.getElementById('box');
        elem.scrollTop = elem.scrollHeight; */
      }
    });
    return false;
  });
/*$(".attach").on('change',function () {
  $("#sendIMG").submit();
    
  });  */

});
  