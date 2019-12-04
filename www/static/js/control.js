// Esperar al que documento HTML este completamente cargado
$(document).ready(function(){

  init();

  function init() {
    getState();
    getSongs();
    selectAll = true; // true = select all items - false = deselect all items
    $('#spinner').hide();
    tiempoRefrescoEstadoEmisora = 1;
    tiempoRefrescoListaCanciones = 10;
    setInterval(getState,tiempoRefrescoEstadoEmisora*1000);
    setInterval(getSongs,tiempoRefrescoListaCanciones*1000);
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

    for (i=0;i<data.length;i++) {

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

  // Obtiene la lista de archivos que se han subido al formulario del navegador
  function getFiles() {
    var fileInput = $('#uploadsongs input[type=file]');
    var file;
    if (fileInput[0].files.length != 0) {
      var formData = new FormData();
      for (i=0; i<fileInput[0].files.length; i++) {
        file = fileInput[0].files[i];
        if (file!=undefined) {
          formData.append('file'+i, file, file.name);
        }
      }
    }
    return formData;
  }

  // Actualiza la parte visual del panel de estado de la emisora
  function updateState(song, frequency, status) {
    var songInfo = "Listening to: " + song;
    var freqInfo = "FM Frequency: " + frequency + " MHz";
    var statusInfo = "";
    if (status === 1) {
      $('#btnPlay').css('display', 'none');
      $('#btnStop').css('display', 'block');
      $('#btnNext').css('display', 'block');
      $('#btnPrev').css('display', 'block');
      statusInfo = "We are online!";
    } else {
      $('#btnPlay').css('display', 'block');
      $('#btnStop').css('display', 'none');
      $('#btnNext').css('display', 'none');
      $('#btnPrev').css('display', 'none');
      statusInfo = "We are offline...";
    }
    $("#songInfo").text(songInfo);
    $("#frequencyInfo").text(freqInfo);
    $("#statusInfo").text(statusInfo);
  }

  // Definicion de peticiones AJAX

  // Realiza un requerimiento HTTP al servidor para obtener el estado de la emisora
  function getState() {
    $.ajax({
      url: '/update',
      type: "GET",
      success: function(data) {
        updateState(data["song"], data["frequency"], data["status"]);        
      },
      error: function(data) {
        alert("No se pudo obtener el estado de la radio");
      }
    });
  }  

  // Realiza un requerimiento HTTP al servidor para obtener la lista de archivos de audio de la emisora
  function getSongs() {
    $.ajax({
      url: '/songs',
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
  function uploadSongs(datos) {
    $('#spinner').show();
    $('#uploadBtn').prop('disabled', true);
    $.ajax({
      url: '/upload',
      type: "POST",
      data: datos,
      contentType: false,
      processData: false,
      success: function(data) {
        updateList(data.songs_list);
        $('#fileInput').val(null); // limpia el input del archivo        
      },
      error: function(data) {
        alert("No se pudo subir el archivo");
      },
      complete: function(data) {
        $('#spinner').hide();
        $('#uploadBtn').prop('disabled', false);
      }
    });
  }

  // Realiza un requerimiento HTTP al servidor para eliminar un conjunto de archivos de audio en la emisora
  function deleteSongs(songs) {
    $.ajax({
      url: '/delete',
      type: "DELETE",
      contentType: "application/json",
      data: JSON.stringify(songs),
      success: function(data) {
        updateList(data.songs_list);
      },
      error: function(data) {
        alert("No se pudo borrar el archivo");
      }
    });
  }

  // Definicion de eventos para los botones de la pagina

  $('#btnPlay').click(function() {
      $.ajax({
        url: '/play',
        type: "GET",
        success: function(data) {
          $("#btnPlay").css("display", "none");
          $("#btnStop").css("display", "block");
          $("#btnNext").css("display", "block");
          $("#btnPrev").css("display", "block");
          $("#statusInfo").text("We are online");
        },
        error: function(data) {
          alert("No se pudo iniciar la radio");
        }
      });
  });

  $('#btnStop').click(function() {
      $.ajax({
        url: '/stop',
        type: "GET",
        success: function(data) {          
          $("#btnPlay").css("display", "block");
          $("#btnStop").css("display", "none");
          $("#btnNext").css("display", "none");
          $("#btnPrev").css("display", "none");
          $("#statusInfo").text("We are offline...");
        },
        error: function(data) {
          alert("No se pudo cerrar la radio");
        }
      });
  });

  $('#btnNext').click(function() {
      $.ajax({
        url: '/next',
        type: "GET"       
      });
  });

  $('#btnPrev').click(function() {
      $.ajax({
        url: '/prev',
        type: "GET"
      });
  });

  $('#deleteBtn').click(function() {
    var songs = getSelected();
    if (songs.length > 0) {
      deleteSongs(songs);
    } else {
      alert("No seleccionaste ninguna cancion");
    }

  });

  $('#selectAllBtn').click(function() {
    $('input[type="checkbox"]').each(function() {
      $(this).prop("checked", selectAll);
    });

    if (selectAll) {
      $('#selectAllBtn').text("Unselect All");
    } else {
      $('#selectAllBtn').text("Select All");
    }

    selectAll = !selectAll;
  });

  $('#uploadBtn').click(function() {
    var datos = getFiles();
    if (datos != undefined) {
      uploadSongs(datos);
    } else {
      alert('No seleccionaste ningun archivo');
    }
  });

});
