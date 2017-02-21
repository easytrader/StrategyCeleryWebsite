$(document).ready(function() {
    //alert("leo test")


    $('.save-strategy').click(function(){
      //alert("leo test 1");
      console.log('am i called');
      var path = window.location.pathname
      var str = path.split("/");
      //alert(str)
      //alert(str[2])
        $.ajax({
            type: "POST",
            url: "/strategy_modify/",
            dataType: "json",
            data: { "strategy_content": editor1.getValue(),"position_content": editor2.getValue(),"pk_key":parseInt(str[2])},
            success: function(data) {
                //alert(data["name"]);
            }
        });

    });

    $('.run-strategy').click(function(){
      //alert("leo test 1");
      console.log('am i called');
      //alert("leo test")
        $.ajax({
            type: "POST",
            url: "/strategy_run/",
            dataType: "json",
            data: { "strategy_content": editor1.getValue(),"position_content": editor2.getValue() ,"tickers": $('input[name="tickers"]').val()},
            beforeSend: function(){
                $('#loadingIMG').show();
            },
            complete: function(){
                $('#loadingIMG').hide();
            },
            success: function (response) {
                 //alert("You will now be redirected.");
                 window.location = "/strategy_run/";

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

