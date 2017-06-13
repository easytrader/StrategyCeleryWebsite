$(document).ready(function() {
$('.daily-run').click(function(){
      alert("leo test daily-run");
      console.log('am i called');
      var url = window.location.pathname;
      var strategy_id = url.substring(url.lastIndexOf('/') + 1);
      //alert(str)
      //alert(str[2])
        $.ajax({
            type: "POST",
            url: "/daily_run_strategy/",
            dataType: "json",
            data: {"strategy_id":strategy_id },
            success: function(data) {
                //alert(data["name"]);
            }
        });

    });

    $('.daily-del').click(function(){
      alert("leo test daily-DEL");
      console.log('am i called');
      var url = window.location.pathname;
      var strategy_id = url.substring(url.lastIndexOf('/') + 1);
      //alert(str)
      //alert(str[2])
        $.ajax({
            type: "POST",
            url: "/del_daily_run_strategy/",
            dataType: "json",
            data: {"strategy_id":strategy_id },
            success: function(data) {
                //alert(data["name"]);
            }
        });

    });
    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

