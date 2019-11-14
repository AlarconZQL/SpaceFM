// Esperar al que documento HTML este completamente cargado
$(document).ready(function(){

  init();

  function init() {
    getState();
    getSongs();
    selectAll = true; // true = select all items - false = deselect all items
    $('#spinner').hide();
    //setInterval(actualizar,1000);
  }

  // Realiza un requerimiento HTTP al servidor para obtener el estado de la emisora
  function getState() {
    var color=0;
    $.ajax({
      url: '/actualizar',
      type: "GET",
      success: function(data) {

        var songInfo = "Listening to: " + data["song"];
        var freqInfo = "FM Frequency: " + data["frequency"] + " MHz";
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

  // Obtiene todos los nombres de archivos de audio que se han seleccionado en la lista
  function getSelected() {
    var selected = [];

    $('#list input:checked').each(function() {
      selected.push($(this).attr('name'));
    });

    return selected;
  }

  // Reconstruye la vista de la lista que contiene a los nombres de los archivos de audio
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

    }
  }

  // Obtiene la lista de archivos que se han subido al navegador
  // Por el momento solo toma el primer elemento de la lista
  function getFiles() {
    var fileInput = $('#uploadsongs input[type=file]');
    var file = fileInput[0].files[0];

    if(file!=undefined) {
      var formData = new FormData();
      formData.append('file', file, file.name);
    }

    return formData;
  }

  // Realiza un requerimiento HTTP al servidor para obtener la lista de archivos de audio de la emisora
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

  // Realiza un requerimiento HTTP al servidor para transferir un archivo de audio a la emisora
  function uploadSong(datos) {
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
      }
    });
  }

  // Realiza un requerimiento HTTP al servidor para eliminar un conjunto de archivos de audio en la emisora
  function deleteSongs(songs) {
    $.ajax({
      url: '/borrar',
      type: "DELETE",
      contentType: "application/json",
      data: JSON.stringify(songs),     
      success: function(data) {
        if (data.songs_list != undefined) {
          updateList(data.songs_list);
        }
      },
      error: function(data) {
        alert("No se pudo borrar el archivo");
      }
    });
  }

  // Definicion de eventos para los botones de la pagina

  $('#deleteBtn').click(function() {
    var songs = getSelected();
    if (songs.length > 0) {
      deleteSongs(songs);
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
      uploadSong(datos);
      $('#uploadBtn').prop('disabled', false);
      $('#spinner').hide();
    } else {
      alert('No seleccionaste ningun archivo');
    }
  });

});
