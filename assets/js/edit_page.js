function pb_hide(){
    setTimeout(function () {
        $("#pb").hide();
        $("#resp_ajax").show();
        $('#edit :input').attr('disabled', false);
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

    $('#not_loged form').submit(function (e) {
        var login_data = new FormData(this);
        e.preventDefault();
        $('#not_loged form :input').attr('disabled', true);
        $.ajax({
            type: "POST",
            processData: false,
            contentType: false,
            url: "/ajax_login",
            data: login_data,
            success: function (result){
                console.log('Succses: '+result['succses'])
                if (!result['succses']) {
                    $('#login_erors').html(result['error'])
                } else {
                    $.get("/edit", function(response){
                        console.log(response);
                        $("body").html(response);

                    });
                };
            },
        });
        $('#not_loged form :input').attr('disabled', false);
    });

    $('#edit').submit(function(e){
        $("#resp_ajax").hide();
        e.preventDefault();
        var formData = new FormData(this);
        $('#edit :input').attr('disabled', true);
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

