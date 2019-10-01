// Wait till the document is fully loaded
$(document).ready(function(){

  init();

  function init() {
    getState();
    getSongs();
    selectAll = true; // true = select all items - false = deselect all items
    $('#spinner').hide();
    //setInterval(actualizar,1000);
  }

  function getState() {
    var color=0;
    $.ajax({
      url: '/actualizar',
      success: function(data) {

        var songInfo = "Listening to: " + data["song"];
        var freqInfo = "FM Frequency: " + data["frecuency"] + " MHz";
        var status =  data["status"];
        var powerBtnColor = "";
        var statusInfo = "";
        if (status === "emiting") {
          powerBtnColor = "red";
          statusInfo = "We are online!";
        } else {
          powerBtnColor = "green";
          statusInfo = "We are offline...";
        }

        $("#songInfo").text(songInfo);
        $("#frequencyInfo").text(freqInfo);
        $("#statusInfo").text(statusInfo);
        $("#powerBtn").css("background-color", powerBtnColor);
      }
    });
  }

  function getSelected() {
    var selected = [];

    $('#list input:checked').each(function() {
      selected.push($(this).attr('name'));
    });

    return selected;
  }

  function updateList(data) {

    var newList = $("#list").empty();

    for(i=0;i<data.length;i++) {

      var song = JSON.parse(data[i]);

      var itemList = $("<li></li>");
      itemList.addClass("list-group-item");

      var songItem = $("<div></div>");
      songItem.addClass("custom-control custom-checkbox");

      var input = $("<input></input>");
      input.addClass("custom-control-input");
      input.attr("id",song.id);
      input.attr("name",song.name);
      input.attr("type","checkbox");

      var label = $("<label></label>");
      label.addClass("custom-control-label");
      label.attr("for",song.id);
      label.text(song.name);

      songItem.append(input, label);
      itemList.append(songItem);
      newList.append(itemList);

      //aux += "<li class=\"list-group-item\" ><div id=\"songsList\" class=\"custom-control custom-checkbox\" ><input type=\"checkbox\" class=\"custom-control-input\" id=\""+dato.id+"\"  name=\""+dato.name+"\" >    <label class=\"custom-control-label\" for=\""+dato.id+"\" >" +dato.name+"</label></div></li>";

    }
    //$('#list').html(aux);
  }

  function actualizar(){
    var color=0;
    $.ajax({
      url: '/actualizar',
      success: function(data){
        var texto = "Song: "+data['song']+"<br>"
        +"Frecuency: "+data['frecuency']+"<br>"
        +"Status: "+data['status']+"<br>";
        $('#estados').html(texto);
        if(color==0) {
          $('#estados').css("color", "red");
          color=1;
        } else {
          $('#estados').css("color", "blue");
          color=0;
        }
      }
    });
  }

  function getFiles() {
    var fileInput = $('#uploadsongs input[type=file]');
    var file = fileInput[0].files[0];

    if(file!=undefined) {
      var formData = new FormData();
      formData.append('file', file, file.name);
    }

    return formData;
  }

  function getSongs() {
    $.ajax({
      url: '/listar',
      type: "GET",
      success: function(data) {
        if (data.songs_list != undefined) {
          updateList(data.songs_list);
        } 
      },
      error: function(data) {
        alert("No se pudieron listar las canciones");
      }
    });
  }

  // Definicion de eventos

  $('#deleteBtn').click(function() {
    var songs = getSelected();
    if (songs.length > 0) {
      $.ajax({
        url: '/borrar',
        data: JSON.stringify(songs),
        contentType: "application/json",
        type: "POST",
        success: function(data) {
          if (data.songs_list != undefined) {
            updateList(data.songs_list);
          }          
        },
        error: function(data) {
          alert("No se pudo borrar el archivo");
        }
      });
    } else {
      alert("No seleccionaste ninguna cancion");
    }
    
  });

  $('#selectAllBtn').click(function() {
    $('input[type="checkbox"]').each(function(){
      $(this).prop("checked", selectAll);
    });

    if (selectAll) {
      $('#selectAllBtn').text("Unselect All");
    } else {
      $('#selectAllBtn').text("Select All");
    }

    selectAll = !selectAll;
  });

  $('#stopBtn').click(function() {
    $.ajax({
      url: '/info',
      success: function(data) {
        $('#prueba').text($('#prueba').text() + data['dato']);
      }
    });
  });    

  $('#uploadBtn').click(function() {
    var datos = getFiles();
    if (datos != undefined)
    {
      $('#uploadBtn').prop('disabled', true);
      $('#spinner').show();
      $.ajax({
        url: '/upload',
        type: "POST",
        data: datos,
        contentType: false,
        processData: false,
        success: function(data) {
          if (data.songs_list != undefined) {
            updateList(data.songs_list);
            $('#file1').val(null); // limpia el input del archivo
          } else {
            alert(data.error_msg);
          }
        },
        error: function(data) {
          alert("No se pudo subir el archivo");
        },
        complete: function(data) {
          $('#uploadBtn').prop('disabled', false);
          $('#spinner').hide();
        }
      });
    } else {
      alert('No seleccionaste ningun archivo');
    }
  });

});
