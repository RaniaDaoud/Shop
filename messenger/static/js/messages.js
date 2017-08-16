$(function () {
  $("#send").submit(function () {
    $.ajax({
      url: '/messages/send/',
      data: $("#send").serialize(),
      cache: false,
      type: 'post',


      success: function (data) {
        //$(".send-message").before(data);
        
        $("#box").append(data);
        
        $("input[name='message']").val('');
        $("input[name='message']").focus();
        $(".success_message").fadeOut().html(data);
        var elem = document.getElementById('box');
        elem.scrollTop = elem.scrollHeight;
        
      }
    });
    return false;
  });
});