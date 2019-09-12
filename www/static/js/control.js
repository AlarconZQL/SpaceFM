



function getSelected() {
  var selected = [];

  $('#list input:checked').each(function() {
      selected.push($(this).attr('name'));
  });
  return JSON.stringify(selected);
}

function updateList(data) {
  $('#list').html("");
  var aux ="";
  for(i=0;i<data.length;i++) {

    var dato=JSON.parse(data[i]);


     aux += "<li class=\"list-group-item\" ><div id=\"songsList\" class=\"custom-control custom-checkbox\" ><input type=\"checkbox\" class=\"custom-control-input\" id=\""+dato.id+"\"  name=\""+dato.name+"\" >    <label class=\"custom-control-label\" for=\""+dato.id+"\" >" +dato.name+"</label></div></li>";

    //debugger;
    //console.log(JSON.parse(data[i]).name);
    //console.log(JSON.parse(data[i]).id);
    //alert(data[i]['id']);
  }
  $('#list').html(aux);




}




$('#deleteBtn').click(function() {
        $.ajax({
          url: '/borrar',
          data: getSelected(),
          contentType: "application/json",
          type: "POST",
          success: function(data) {
        updateList(data);
          }
        });

    });





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
 //setInterval(actualizar,1000);
});


$('#stop').click(function() {
        $.ajax({
          url: '/info',
          success: function(data) {
              $('#prueba').text($('#prueba').text() + data['dato']);
          }
        });
    });
