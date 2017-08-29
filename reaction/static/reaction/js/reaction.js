$(function () {
    
    $('.reaction-button').on('click', function () {
      var $this = $(this);
      var type = $this.attr('data-reaction');
      var productId = $this.attr('data-id');
      $.ajax({
          url: '/react/' + productId,
          data: {
              'reaction': type
          },
          success: function (data) {
            
            if (data.count > 0)
              $this.parent().siblings('.reactions').children('.badge').text(data.count);
            else
              $this.parent().siblings('.reactions').children('.badge').text('');
                
            $this.parent().children('.reaction-button').children('.tooltip-normal').text("normal ("+ data.count1 +")" );
            $this.parent().children('.reaction-button').children('.tooltip-love').text("love ("+ data.count2 +")" );
            $this.parent().children('.reaction-button').children('.tooltip-smile').text("smile ("+ data.count4 +")" );
            $this.parent().children('.reaction-button').children('.tooltip-wish').text("wish ("+ data.count3 +")" );          
          }
      })
    });
});