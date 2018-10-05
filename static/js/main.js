$(document).ready(function(){

    $('#link_signup').click(function(){
        $('#loginbox').hide();
        $('#signupbox').show();
    });
    $('#link_signin').click(function(){
        $('#loginbox').show();
        $('#signupbox').hide();
    });

    $(document).on("change", "#inst", function(){
        csrftoken = getCookie('csrftoken');
        select = $('#branch');
        select.find('option').remove().end().append(new Option('-- select --', 'select', true, true));
        $.ajax({
            type: "POST",
            url: "/get_branches",
            data: {id : $(this).val(), 'csrfmiddlewaretoken': csrftoken},
            'dataType': 'json',
            success: function(response){
                $.each(response.branches, function(id, val){
                    select.append(new Option(val, id, true, true));
                });
                select.val(select.children().first().val());
            }
        });
        return false;
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
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
});

