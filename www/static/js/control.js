

var color=0;

function actualizar(){
 $.ajax({
  url: '/actualizar',
  success: function(data){
    var texto = "Song: "+data['song']+"<br>"
    +"Frecuency: "+data['frecuency']+"<br>"
    +"Status: "+data['status']+"<br>";
    $('#estados').html(texto);
    if(color==0){
      $('#estados').css("color", "red");
      color=1;

    }
    else
    {
      $('#estados').css("color", "blue");
      color=0;


    }

  }
 });
}

$(document).ready(function(){
 setInterval(actualizar,2000);
});


$('#stop').click(function() {
        $.ajax({
          url: '/info',
          success: function(data) {
              $('#prueba').text($('#prueba').text() + data['dato']);
          }
        });
    });
