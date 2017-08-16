$(function () {
  function check_messages() {
    $.ajax({
      url: '/messages/check/',
      cache: false,
      success: function (data) {
        if (data > 0) {
        $("#unread-count").text(data).show();
      };
      },
      complete: function () {
        window.setTimeout(check_messages, 60000);
      }
    });
  };
  check_messages();
});