 $(function () {

          
  // faire entrer la valeur du slider
            function setValues() {
              var value = $("#ex2").val();
              var value_list = value.split(',');
              $("#min-price").val(parseInt(value_list[0]));
              $("#max-price").val(parseInt(value_list[1]));
            }

            function updateSlider() {
              var min = $("#min-price").val();
              var max = $("#max-price").val();
              var value = [min, max];
              $("#ex2").slider('setValue', value, true);
              $('#myid').slider('refresh');
            }

             $("#ex2").slider({ });
             

            $("#ex2").on('slide', function (e) {
              console.log($(this).val());
              setValues();
            });

            $("#min-price").on('change', function (e) {
              updateSlider();
            });

            $("#max-price").on('change', function (e) {
              updateSlider();
            });   


});
