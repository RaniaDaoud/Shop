/*$(function () {
    $('#comment-form').on('submit', function (e) {
        e.preventDefault();
        var $this = $(this);
        var postId = $this.attr('data-post-id');
        var text = $('#content').val();
        $.ajax({
            url: '/post/postDetail/' + postId ,
            type: 'GET',
            data: {
                text: text
            },
            dataType: 'json',
            success: function (data) {
                if (data.success) {
                    $('#content').val('');
                    $('.comments').prepend(data.comment);
                }
            }
        });
    });
}); */

$(function () {
  $("#comment-form").on('submit',function (comm) {
    comm.preventDefault();
    var $this = $(this);
    var postId = $this.attr('data-post-id');
    /*var data = {
      text: $this.children("#text").val(),
    } */
    $.ajax({
      url: '/post/postDetail/' + postId + '/comment/',
      data: $("#comment-form").serialize(),
      cache: false,
      type: 'post',


      success: function (data) {
         $('.comments').prepend(data);
         $("input[name='text']").val('');
         $('#text').val('');
        
      }
    });
    return false;
  });
});