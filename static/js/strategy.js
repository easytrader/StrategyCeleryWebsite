$(document).ready(function() {
    //alert("leo test")



    $('.del-strategy').click(function(){
      //alert("leo test 1");
      console.log('am i called');
      //alert("leo test")
      //document.getElementById('strategy_checkbox').checked;
      var checkedValue = $('.strategy_checkbox:checked').val();
      //alert(checkedValue.toString());
        $.ajax({
            type: "POST",
            url: "/strategy/del/",
            dataType: "json",
            data: { "checkedValue":checkedValue  },
            success: function(data) {
                //alert("leo test in success");
                //alert("You will now be redirected.");
                window.location = "/strategy/";
            },
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

