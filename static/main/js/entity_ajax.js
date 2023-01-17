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

    $(document).on("click","#update_entity",function(event){
        event.preventDefault();

        const entity_id = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: "/update_entity/",
            method: "POST",
            data: {
                entity_id:entity_id,
            },
            mode: 'same-origin',
            headers: {'X-CSRFToken': csrf},
            dataType: "json",
            statusCode:{
                404: function(){
                    Toast.fire({
                        icon: 'warning',
                        title: ERROR_NOT_FOUND
                    })
                }
            },
            cache: false,
        }).done(function(responce){
            if(responce.status == "success"){

                Toast.fire({
                    icon: 'success',
                    title: SUCCESS_MESSAGE_GET
                })

                $("#id_UpdateEntityModal").modal("show")
                $("#id_modalEntity_header").text("Edit the entity information")

                $("#entity_id").val(responce.info[0]['entity_id'])
                $("#id_entity_name").val(responce.info[0]['entity_name'])

            }
        }).fail(function(responce){
            if(responce.status == "bad_request"){
                Toast.fire({
                    icon: 'error',
                    title: ERROR_FAILDED
                })
            }
        })

    });

    $(document).on("click","#delete_entity",function(event){
        event.preventDefault()

        const entity_id = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: '/delete_entity/',
            method: 'POST',
            data: {
                entity_id:entity_id
            },
            headers: {'X-CSRFToken': csrf},
            mode: 'same-origin',
            statusCode: {
                404: function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    })
                }
            },
            cache: false,
            dataType: 'json'
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
                    title: ERROR_MESSAGE
                })
            }
        })
    });

    $(document).on("submit","#id_UpdateEntityForm", function(event){
        event.preventDefault();

        const entity_id = $("#entity_id").val()
        const entity_name = $("#id_entity_name").val()
        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: "/execute_update_entity/",
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            mode: 'same-origin',
            data: {
                entity_id:entity_id,
                entity_name:entity_name,
            },
            cache: false,
            dataType: "json",
            statusCode: {
                404: function(){
                    Toast.fire({
                        icon: 'warning',
                        title: ERROR_NOT_FOUND
                    })
                }
            }
        }).done(function(responce){
            if(responce.status == "success"){
                Toast.fire({
                    icon: 'success',
                    title: SUCCESS_MESSAGE_POST
                })

                reloadPage()
            }

            Toast.fire({
                icon: "warning",
                title: responce["entity_name"][0]['message']
            })

        }).fail(function(responce){
            if(responce.status == "bad_request"){

                Toast.fire({
                    icon: 'error',
                    title: ERROR_FAILDED
                })

            }
        });
    });

});