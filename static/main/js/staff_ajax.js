function reloadPage(){
    setInterval(function(){
        window.location.reload()
    },3000)
}

$(document).ready(function(){

    const ERROR_NOT_FOUND = "Error 404 request not found! please try again."
    const ERROR_FAILDED = "Failed! you have an unsuccessful request."
    const SUCCESS_MESSAGE_GET = "Success! you have successfully get the information."
    const SUCCESS_MESSAGE_POST = "Success! you have successfully updated the information"
    const SUCCESS_MESSAGE_ADD = "Success! you have successfully add the information"
    const SUCCESS_DELETE_MESSAGE = "Success! you have successfully deleted the information"


    var Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 6000
    });

    $(document).on("click","#update_staff",function(event){
        event.preventDefault();

        const complainant = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        $.ajax({
            url: '/update_staff/',
            method: 'POST',
            data: {
                complainant:complainant,
            },
            statusCode: {
                404: function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    });
                }
            },
            headers: {'X-CSRFToken':csrf},
            mode: 'same-origin'
        }).done(function(responce){

            if(responce.status == "success"){
                Toast.fire({
                    icon: "success",
                    title: SUCCESS_MESSAGE_GET
                })

                $("#id_UpdateStaffForm").modal("show")
                $("#id_modalStaff_header").html("Edit the staff information")

                $("#staff_id").val(responce.info[0]['staff_id'])
                $("#id_staff_name").val(responce.info[0]['staff_name'])
            }

        }).fail(function(responce){

            if(responce.status == "bad_request"){
                Toast.fire({
                    icon: "error",
                    title: ERROR_FAILED
                })
            }

        })
    });


    $(document).on("click","#id_UpdateStaffForm",function(event){
        event.preventDefault();

        const staff_id = $("#staff_id").val()
        const staff_name = $("#id_staff_name").val()
        const staff_position = $("#id_staff_position").val()

        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        $.ajax({
            url: '/execute_update_staff/',
            method: 'POST',
            data: {
                staff_id:staff_id,
                staff_name:staff_name,
                staff_position:staff_position
            },
            statusCode: {
                404: function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    });
                }
            },
            headers: {'X-CSRFToken':csrf},
            mode: 'same-origin'
        }).done(function(responce){

            if(responce.status == "success"){
                Toast.fire({
                    icon: "success",
                    title: SUCCESS_MESSAGE_POST
                })

                reloadPage()
            }

        }).fail(function(responce){

            if(responce.status == "bad_request"){
                Toast.fire({
                    icon: "error",
                    title: ERROR_FAILED
                })
            }
            
        })
    });


    $(document).on("click","#delete_staff",function(event){
        event.preventDefault();
        const complainant = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        $.ajax({
            url: '/delete_staff/',
            method: 'POST',
            data: {
                complainant:complainant
            },
            statusCode: {
                404: function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    });
                }
            },
            headers: {'X-CSRFToken':csrf},
            mode: 'same-origin'
        }).done(function(responce){
            if(responce.status == "success"){
                Toast.fire({
                    icon: "success",
                    title: SUCCESS_DELETE_MESSAGE
                })

                reloadPage()
            }
        }).fail(function(responce){
            if(responce.status == "bad_request"){
                Toast.fire({
                    icon: "error",
                    title: ERROR_FAILED
                })
            }
        })
    });
});