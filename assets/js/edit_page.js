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
        $.ajax({
            type: "POST",
            processData: false,
            contentType: false,
            url: "/edit",
            data:  formData,
            success: function (result){
                pb_hide();
                console.log(result);
                if (result['succses']) {
                    $("#photo").prop('src', result["photo"]);
                    $("#resp_ajax").html("<h2>All data have saved</h2>");
                } else {
                    console.log("EROORS: "+result['errors']);

                    $("#resp_ajax").html(result['errors']);

                };

            },
        });

    });
});

