function setTitle(newtitle) {
     if (document.title != newtitle) {
          document.title = newtitle;
     };
};

var active = true;
var repeatAjax;
function sendAjax() {
     $.getJSON('req_json', function(data) {
          setTitle(data['new_title']);
          $('#req_list').html(data['new_requests_list']);
     })
     .always(function() {
        if (!active) {
            repeatAjax = setTimeout(sendAjax, 1000);
        };
     });
};

$(window).blur(function(){
    active = false;
    $.getJSON('req_json', {window_state:'inactive'});
    sendAjax();
});

$(window).focus(function(){
    active = true;
    clearTimeout(repeatAjax);
    $.getJSON('req_json', {window_state:'active'});
    setTitle("Requests");
});


