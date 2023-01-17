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

    $(document).on("click","#update_complaint",function(event){
        event.preventDefault();

        const complaint_id = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: "/update_complaint/",
            method: "POST",
            data: {
                complaint_id:complaint_id,
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

                $("#id_modalComplaint_change").modal("show")
                $("#id_modalComplaint_header").text("Edit the complaint information")
                $("#complaint_id").val(responce.info[0]['complaint_id'])
                $("#id_case_no").val(responce.info[0]['case_no'])
                $("#id_complaint_desc").val(responce.info[0]['complaint_desc'])
                $("#id_settlement_desc").val(responce.info[0]['settlement_desc'])
            }

            if(responce.status == "error"){
                Toast.fire({
                    icon: 'error',
                    title: ERROR_FAILDED
                })
            }
        }).fail(function(){
            Toast.fire({
                icon: 'error',
                title: ERROR_FAILDED
            })
        })

    });


    $(document).on("submit","#id_UpdateComplaintForm", function(event){
        event.preventDefault();

        const complaint_id = $("#complaint_id").val()
        const case_no = $("#id_case_no").val()
        const complainant = $("#id_complainant").val()
        const respondent = $("#id_respondent").val()

        const complaint_status = $("#id_complaint_status").val()
        const complaint_type = $("#id_complaint_type").val()
        const hearing_schedule = $("#id_hearing_schedule").val()
        const complaint_desc = $("#id_complaint_desc").val()
        const settlement_desc = $("#id_settlement_desc").val()
        const purok = $("#id_purok").val()
        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: "/execute_update_complaint/",
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            mode: 'same-origin',
            data: {
                complaint_id:complaint_id,
                case_no:case_no,
                complaint_desc:complaint_desc,
                complainant:complainant,
                complaint_status:complaint_status,
                hearing_schedule:hearing_schedule,
                complaint_type:complaint_type,
                purok:purok,
                respondent:respondent,
                settlement_desc:settlement_desc,
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

            if(responce["case_no"]){
                Toast.fire({
                    icon: "error",
                    title: "The case number you provided is already in the database, please choose a new one and try again. :)"
                })
            }


        }).fail(function(responce){
            if(responce.status == "bad_request"){

                Toast.fire({
                    icon: 'error',
                    title: ERROR_MESSAGE
                })

            }
        });
    });

    $(document).on("click","#delete_complaint",function(event){
        event.preventDefault()

        const complaint_id = $(this).data("id")
        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: '/delete_complaint/',
            method: 'POST',
            data: {
                complaint_id:complaint_id
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

    $(document).on("submit","#id_add_complaint_form",function(event){
        event.preventDefault();

        const complaint_id = $("#complaint_id").val()
        const case_no = $("#id_case_no").val()
        const complainant = $("#id_complainant").val()
        const respondent = $("#id_respondent").val()
        const complaint_status = $("#id_complaint_status").val()
        const complaint_type = $("#id_complaint_type").val()
        const complaint_desc = $("#id_complaint_desc").val()
        const settlement_desc = $("#id_settlement_desc").val()

        const hearing_schedule = $("#id_hearing_schedule").val()
        const purok = $("#id_purok").val()

        const csrf = $("input[name=csrfmiddlewaretoken]").val()

        $.ajax({
            url: '/add_complaint/',
            method: 'POST',
            data: {
                complaint_id:complaint_id,
                case_no:case_no,
                complaint_desc:complaint_desc,
                complainant:complainant,
                complaint_status:complaint_status,
                complaint_type:complaint_type,
                respondent:respondent,
                hearing_schedule:hearing_schedule,
                purok:purok,
                settlement_desc:settlement_desc
            },
            headers: {'X-CSRFToken': csrf},
            mode: 'same-origin',
            cache: false,
            dataType: 'json',
            statusCode: {
                404: function(){
                    Toast.fire({
                        icon: "warning",
                        title: ERROR_NOT_FOUND
                    })
                }
            }
        }).done(function(responce){

            if(responce.status == "success"){
                Toast.fire({
                    icon: "success",
                    title: SUCCESS_MESSAGE_ADD
                })

                reloadPage()
            }

            if(responce["case_no"]){
                Toast.fire({
                    icon: "error",
                    title: "The case number you provided is already in the database, please choose a new one and try again. :)"
                })
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

});