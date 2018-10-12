$(document).ready(function(){

    $('#link_signup').click(function(){
        $('#loginbox').hide();
        $('#signupbox').show();
    });
    $('#link_signin').click(function(){
        $('#loginbox').show();
        $('#signupbox').hide();
    });

    $(document).on("click", ".check-fee", function(e){


        total = parseFloat($('#total_amount').val());

//        if(total==0.0 && parseFloat($('#span_total').text())

        if($(this).is(':checked')){
            total += parseFloat($(this).val());
        }
        else{
            total -= parseFloat($(this).val());
        }

        $('#total_amount').val(total);
        $('#span_total').text(total);

    });

    $(document).on("submit", "#fr_pass_form", function(e){
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/send_pass_reset_mail",
            data: $(this).serialize(),
            dataType: 'json',

            success: function(response){
                if(response.success){
                    $('#lbl_pass_reset_info').show();
                }
                else{
                    $('#lbl_pass_reset_info').show();
                    $('#lbl_pass_reset_info').text('Enter Valid username or email');
                }
            }
        });
    });


//    $(document).on("submit", "#pay_fee_form", function(e){
//        e.preventDefault();
//
//        $.ajax({
//            type: "POST",
//            url: "/create_payment",
//            data: {$(this).serialize(), 'csrfmiddlewaretoken': csrftoken}
//            dataType: 'json',
//
//            success: function(response){
//                alert('Success');
//            }
//        });
//    });


    $(document).on("change", "#inst", function(){
        csrftoken = getCookie('csrftoken');
        select = $('#branch');
        select.find('option').remove().end().append(new Option('-- select --', 'select', true, true));
        $.ajax({
            type: "POST",
            url: "/get_branches",
            data: {id : $(this).val(), 'csrfmiddlewaretoken': csrftoken},
            dataType: 'json',
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

