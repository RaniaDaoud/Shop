$(function () {
    $('.item-close').on('click', function () {
    var $this = $(this);
    var itemId = $this.attr('data-item-id');

    $.ajax({
        url: '/album/delete/' + itemId,
        type: 'POST',
        success: function (data) {

            $this.closest('.item').remove();
            
        }
    });

});
});
