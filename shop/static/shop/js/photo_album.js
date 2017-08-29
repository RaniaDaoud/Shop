function add(input, url, $item) {
    var length = input.files.length;

    for (var i=0; i<length; i++) {
        var formData = new FormData();
        formData.append('image', input.files[i]);
        
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            cache: false,
            success: function (data) {
                if (data.success) {
                    $item.children('.item-close').attr('data-item-id', data.id);
                }
            }
        });
    }
}

function remove($this, url) {
    $.ajax({
        url: url,
        type: 'POST',
        success: function (data) {
            $this.parent('.item').remove();
            if ($('.item').length === 0)
                $('.hint-div').show();
        }
    });
}

$(function () {
    $('.items').on('click', '.item-close', function () {
        var $this = $(this);
        var itemId = $this.attr('data-item-id');
        var url = removeURL.replace('(id)', itemId);

        console.log(url);

        if (confirm('Are you sure?')) {
            remove($this, url)
        }
    });

    $('#file_input').on('change', function () {
        var $item = $('.item').last().clone().show();
        $('.hint-div').hide();
        add(this, addURL, $item);
        previewMultiple(this, $('.items'), $item);
    });
});