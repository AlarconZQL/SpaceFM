$(document).ready(function(){
    $("#western-select").change(function() {                    
        $('#western-img').attr('src', "data:image/png;base64,"+$(this).find(":selected").attr('data-image'));
    });
    $("#western-select").change();

    $("#eastern-select").change(function() {
        $('#eastern-img').attr('src', "data:image/png;base64,"+$(this).find(":selected").attr('data-image'));
    });
    $("#eastern-select").change();
});