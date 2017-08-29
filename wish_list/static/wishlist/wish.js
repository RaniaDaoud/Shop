/*$(function (){
     console.log('test');
$('.wish').on('submit', function (e) {
        e.preventDefault();
        var $this = $(this);
        var $checkbox = $this.children('input[type="checkbox"]');
        var itemId = $this.attr('data-product-id');
        var wishId = $this.attr('data-wish-id');
        if ($checkbox.is(':checked'))
           var  url = '/whishlist/' + wishId  +'/'+ itemId ;
        else
            var url = '/whishlist/add_to_wishlist/' + itemId +'/';
           
        $.ajax({
            url: url,
            type: 'POST',
            data: $(".wish").serialize(),
            dataType :'json' ,
            success: function (data) {
                if (data.success) {
                    $this.children('input[type="checkbox"]').prop('checked', data.checked);
                }
            }
        });
    });   

});   */