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
          var req_list=data['new_requests_list']
          var req_list_html='';
          for (var i=0; i<req_list.length; i++) {
              req_list_html+='<p>'+req_list[i]+'</p>'
          };
          $('#req_list').html(req_list_html);
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


