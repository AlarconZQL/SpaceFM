// Wait till the document is fully loaded
$(document).ready(function(){

  init();

  function init() {
    updateState();
    selectAll = true; // true = select all items - false = deselect all items
    //setInterval(actualizar,1000);
  }

  function updateState() {
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
    return JSON.stringify(selected);
  }

  function updateList(data) {
    $('#list').html("");
    var aux ="";

    var newList = $("#list").empty();

    for(i=0;i<data.length;i++) {

      var dato=JSON.parse(data[i]);

      var itemList = $("<li></li>");
      itemList.addClass("list-group-item");

      var songItem = $("<div></div>");
      songItem.addClass("custom-control custom-checkbox");

      var input = $("<input></input>");
      input.addClass("custom-control-input");
      input.attr("id",dato.id);
      input.attr("name",dato.name);
      input.attr("type","checkbox");

      var label = $("<label></label>");
      label.addClass("custom-control-label");
      label.attr("for",dato.id);
      label.text(dato.name);

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

  function getFiles() {
    var fileInput = $('#uploadsongs input[type=file]');
    var file = fileInput[0].files[0];

    if(file!=undefined) {
      var formData = new FormData();
      formData.append('file', file, file.name);
    }

    return formData;
  }
  $('#spinner').hide();

  $('#uploadBtn').click(function() {
    var datos = getFiles();
    if (datos!=undefined)
    {
      $('#uploadBtn').prop('disabled', true);
      $('#spinner').show();
      $.ajax({
        url: '/upload',
        type: "POST",
        data: getFiles(),
        contentType: false,
        processData: false,
        success: function(data) {
        }
        ,
        error: function(data) {
            console.log("NÃO FUNFOU!");
        },
        complete: function(data) {
          $('#uploadBtn').prop('disabled', false);
          $('#spinner').hide();
          alert(data);

            //A function to be called when the request finishes
            // (after success and error callbacks are executed).
        }
      });
    } else {
      alert('no files selected');
    }
  });

});
