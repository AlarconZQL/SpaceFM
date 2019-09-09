
$('#stop').click(function() {
        $.ajax({
          url: '/info',
          success: function(data) {
              $('#prueba').text($('#prueba').text() + data['dato']);
          }
        });
    });
