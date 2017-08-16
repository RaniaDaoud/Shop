$(function () {
    
    $('.reaction-button1').on('click', function () {
      var $this = $(this);
      var type = $this.attr('data-reaction');
      var postId = $this.attr('data-id');

      $.ajax({
          url: '/reactPost/' + postId,
          data: {
              'reaction': type
          },
          cache: false,
          success: function (data) {
              console.log(data);
            if (data.count > 0)
              $this.parent().siblings('.reactions1').children('.badge').text(data.count);
            else
              $this.parent().siblings('.reactions1').children('.badge').text('');
                
            $this.parent().children('.reaction-button1').children('.tooltip-like').text("like ("+ data.count1 +")" );
            $this.parent().children('.reaction-button1').children('.tooltip-dislike').text("dislike ("+ data.count2 +")" );
           // $this.parent().children('.reaction-button').children('.tooltip-smile').text("smile ("+ data.count4 +")" );
           // $this.parent().children('.reaction-button').children('.tooltip-wish').text("wish ("+ data.count3 +")" );          
          }
      })
    });
});