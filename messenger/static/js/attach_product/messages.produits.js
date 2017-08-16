// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});







$(function () {


  
  $(".sendMes").on('click', function () {
    var $this = $(this);
    var data = {
    	to: $this.children("#to").val(),
    	objet: $this.children("#objet").val(),
    	url: $this.children("#url").val()
    }
    $.ajax({
      url: '/messages/sendMes/',
      data: data,
      cache: false,
      type: 'post',
      success: function (data) {
      //  $feed = alert("succefully submitted");
     //   $(".send-message").before(data);
        $(".success_message").fadeOut().html(data);
        $("input[name='message']").val('');
        $("input[name='message']").focus();
        $(".myBox").append(data);
        var elem = document.getElementById('box');
        elem.scrollTop = elem.scrollHeight;
      //  $this.prepend($feed);
      }  
    });
    return false;
  });
});