function pb_hide(){
    setTimeout(function () {
        $("#pb").hide();
        $("#resp_ajax").show();
    }, 2000);
};


function pb_show(){
        $("#pb").show();
    };



$(document).ready(function ($) {

    $("#id_birth_date").datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd",
        showButtonPanel: true,
        yearRange: "-65:-14",
        firstDay: 1,
        showAnim: 'slideDown',
    });

    $('#edit').submit(function(e){
        $("#resp_ajax").hide();
        e.preventDefault();
        var formData = new FormData(this);

        pb_show();
        pb_hide();
    });
});

