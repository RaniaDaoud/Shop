 $(function () {
    $('.reaction-button').on('mouseenter', function () {
      var tooltip = $(this).attr('data-tooltip');
      $(this).children('.' + tooltip).show();
    });

    $('.reaction-button').on('mouseleave', function () {
      var tooltip = $(this).attr('data-tooltip');
      $(this).children('.' + tooltip).hide();
    });
  });


  $(function () {
    $('.reaction-button1').on('mouseenter', function () {
      var tooltip = $(this).attr('data-tooltip');
      $(this).children('.' + tooltip).show();
    });

    $('.reaction-button1').on('mouseleave', function () {
      var tooltip = $(this).attr('data-tooltip');
      $(this).children('.' + tooltip).hide();
    });
  });