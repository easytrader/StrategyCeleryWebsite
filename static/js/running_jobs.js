$(document).ready(function() {
    //alert("leo test")

    $('.del-aps').click(function(){
        // Get the number starting from the ID's 6th character
        // This assumes that the common prefix is "mydiv"
        //var i = Number(this.id);

        //alert('you clicked ' + i);
        alert('del-aps');
        $.ajax({
            type: "POST",
            url: "/aps/del/",
            dataType: "json",
            data: {"job-id":this.id},
            success: function(data) {
                //alert("leo test in success");
                //alert("You will now be redirected.");
                window.location = "/running_jobs/";
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

