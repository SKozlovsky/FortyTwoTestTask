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

    $('#edit').submit(function(e){
        $("#resp_ajax").hide();
        e.preventDefault();
        var formData = new FormData(this);

        pb_show();
        pb_hide();
    });
});

