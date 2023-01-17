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

    $(document).on("click","#update_respondent",function(event){
        event.preventDefault()
        const respondent = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        $.ajax({
            url: '/update_respondent/',
            method: 'POST',
            data: {
                respondent:respondent
            },
            statusCode:{
                404:function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    })
                }
            },
            headers: {'X-CSRFToken':csrf},
            mode: 'same-origin',
            dataType: 'json',
            cache: false 
        }).done(function(responce){
            if(responce.status == "success"){

                Toast.fire({
                    icon: "success",
                    title: SUCCESS_MESSAGE_GET
                })

                $("#id_UpdateRespondentModal").modal("show")
                $("#id_modalRespondent_header").html("Edit the respondent information")

                $("#respondent_id").val(responce.info[0]['respondent_id'])
                $("#id_respondent_name").val(responce.info[0]['respondent_name'])
            }
        }).fail(function(responce){
            if(responce.status == "bad_request"){
                Toast.fire({
                    icon: "error",
                    title: ERROR_FAILDED
                })
            }
        })
    });

    $(document).on("click","#delete_respondent",function(event){
        event.preventDefault()
        const respondent = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()
        $.ajax({
            url: '/delete_respondent/',
            method: 'POST',
            data: {
                respondent:respondent
            },
            statusCode:{
                404:function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    })
                }
            },
            headers: {'X-CSRFToken':csrf},
            mode: 'same-origin',
            dataType: 'json',
            cache: false 
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
                    title: ERROR_FAILDED
                })
            }
        })
    });


    $(document).on("submit","#id_UpdateRespondentForm",function(event){
        event.preventDefault()
        const respondent_id = $("#respondent_id").val()
        const respondent_name = $("#id_respondent_name").val()
        const respondent_purok = $("#id_respondent_purok").val()
        const respondent_barangay = $("#id_respondent_barangay").val()

        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: '/execute_update_respondent/',
            method: 'POST',
            data: {
                respondent_id:respondent_id,
                respondent_name:respondent_name,
                respondent_purok:respondent_purok,
                respondent_barangay:respondent_barangay
            },
            statusCode:{
                404:function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    })
                }
            },
            headers: {'X-CSRFToken':csrf},
            mode: 'same-origin',
            dataType: 'json',
            cache: false 
        }).done(function(responce){
            if(responce.status == "success"){
                Toast.fire({
                    icon: "success",
                    title: SUCCESS_MESSAGE_POST
                })

                reloadPage()
            }

            Toast.fire({
                icon: "warning",
                title: responce["respondent_name"][0]['message']
            })

        }).fail(function(responce){
            if(responce.status == "bad_request"){
                Toast.fire({
                    icon: "error",
                    title: ERROR_FAILDED
                })
            }
        })
    });

});