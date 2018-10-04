$(document).ready(function(){

    person_table = $('#person_table');
    data_table = person_table.DataTable();

    tbl_btn_update = '';

    $(document).on("click", ".btn_delete", function (){
        id = $(this).attr('data');
        btn_dlt = $(this);
        $.ajax({
            type: "POST",
            url: "/delete_person",
            data: {id : id},

            success: function(response){
                btn_dlt.parent().parent().remove();
            }
        });
        return false;
    });

    $(document).on("submit", "#create_form", function (e){
        e.preventDefault();
        modal = $('#registerModal');
        $.ajax({
            type: "POST",
            url: "/create_person",
            data: $(this).serialize(),

            success: function(response){
                var btn = "<button class='btn btn-sm btn-info btn_update_modal' data='"+response.id+"'>Edit</button>&nbsp;&nbsp;&nbsp;"+
                            "<button class='btn btn-sm btn-danger btn_delete' data='"+response.id+"'>Delete</button>&nbsp;";
                modal.modal('hide');
                data_table.row.add(
                    [response.name, response.email, response.mobile,
                     response.gender, response.bld_group, response.dob, btn]).draw(true);
            }
        });
        return false;
    });


    $(document).on("submit", "#update_form", function (e){
        e.preventDefault();
        modal = $('#updateModal');

        $.ajax({
            type: "POST",
            url: "/update_person",
            data: $(this).serialize(),

            success: function(response){
                modal.modal('hide');
                tr = tbl_btn_update.parent().parent();
                $(tr.children()[0]).text(response.name);
                $(tr.children()[1]).text(response.email);
                $(tr.children()[2]).text(response.mobile);
                $(tr.children()[3]).text(response.gender);
                $(tr.children()[4]).text(response.bld_group);
                $(tr.children()[5]).text(response.dob);
            }
        });
        return false;
    });

    $(document).on("click", ".btn_update_modal", function (){
        var id = $(this).attr('data');

        tbl_btn_update = $(this);

        modal = $('#updateModal');

        $.ajax({
            type: "POST",
            url: "/update_person",
            data: {id : id, 'req_type': 'get_update_data'},

            success: function(response){
                modal.modal();
                modal.find('#rec_id').val(response.id);
                modal.find('#name').val(response.name);
                modal.find('#email').val(response.email);
                modal.find('#address').val(response.address);
                modal.find('#mobile').val(response.mobile);
                modal.find('#dob').val(response.dob);
                modal.find('#bldgroup').val(response.bld_group);

                if(response.gender == "M"){
                    modal.find('#male').attr('checked', true);
                }
                else{
                    modal.find('#female').attr('checked', true);
                }
            }
        });
        return false;
    });
});

