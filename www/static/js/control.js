// Esperar al que documento HTML este completamente cargado
$(document).ready(function(){

  init();

  function init() {
    getState();
    getSongs();
    selectAll = true; // true = select all items - false = deselect all items
    $('#spinner').hide();
    //setInterval(getState,1000);
    //setInterval(getSongs,10000);
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
    var file;
    var formData = new FormData();
    for (i=0; i<fileInput[0].files.length; i++) {
      file = fileInput[0].files[i];
      if(file!=undefined) {
        formData.append('file'+i, file, file.name);
      }
    }
    return formData;
  }

  // Definicion de peticiones AJAX

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
        if (status === 1) {
          $('#powerBtnStart').css('display', 'none');
          $('#powerBtnStop').css('display', 'block');
          $('#powerBtnNext').css('display', 'block');
          $('#powerBtnPrev').css('display', 'block');
          statusInfo = "We are online!";
        } else {
          $('#powerBtnStart').css('display', 'block');
          $('#powerBtnStop').css('display', 'none');
          $('#powerBtnNext').css('display', 'none');
          $('#powerBtnPrev').css('display', 'none');
          statusInfo = "We are offline...";
        }

        $("#songInfo").text(songInfo);
        $("#frequencyInfo").text(freqInfo);
        $("#statusInfo").text(statusInfo);
      }
    });
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
    $('#spinner').show();
    $('#uploadBtn').prop('disabled', true);
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
          alert(data);
        }
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

  $('#powerBtnStart').click(function() {
      $.ajax({
        url: '/start',
        type: "POST",
        success: function(data) {
          alert("Radio iniciada!")
          $("#powerBtnStart").css("display", "none");
          $("#powerBtnStop").css("display", "block");
          $("#powerBtnNext").css("display", "block");
          $("#powerBtnPrev").css("display", "block");
          $("#statusInfo").text("We are online!");
        },
        error: function(data) {
          alert("No se pudo iniciar la radio");
        }
      });
  });

  $('#powerBtnStop').click(function() {
      $.ajax({
        url: '/stop',
        type: "POST",
        success: function(data) {

          $("#powerBtnStart").css("display", "block");
          $("#powerBtnStop").css("display", "none");
          $("#powerBtnNext").css("display", "none");
          $("#powerBtnPrev").css("display", "none");
          $("#statusInfo").text("We are offline ... !");
        },
        error: function(data) {
          alert("No se pudo cerrar la radio");
        }
      });
  });

  $('#powerBtnNext').click(function() {
      $.ajax({
        url: '/next',
        type: "POST",
        success: function(data) {

        },
        error: function(data) {
          alert("No se pudo cerrar la radio");
        }
      });
  });

  $('#powerBtnPrev').click(function() {
      $.ajax({
        url: '/prev',
        type: "POST",
        success: function(data) {

        },
        error: function(data) {
          alert("No se pudo cerrar la radio");
        }
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
      uploadSong(datos);
    } else {
      alert('No seleccionaste ningun archivo');
    }
  });

});
