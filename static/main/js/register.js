$(function(){
    'use strict';

    $(document).on("submit","#register_form", function(e){
        e.preventDefault();

        $.ajax({
            headers: {'X-CSRFToken': '{{ csrf_token }}'},
            method: "POST",
            data: $(this).serialize(),
            success:function(responce){
                alert(responce)
            }
        });
    });
})