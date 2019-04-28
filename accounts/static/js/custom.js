$(document).ready(function(){
  var productForm = $(".form-note-ajax")
  var submitButton = productForm.closest('form').find(':submit');


  productForm.submit(function(event){
    event.preventDefault();



    var thisForm = $(this);

    var actionEndpoint = thisForm.attr("action");
    var httpMethod = thisForm.attr("method");
    var formData = thisForm.serialize();
     $.ajax({

       url : actionEndpoint,
       method : httpMethod,
       data : formData,

       success : function(data){
            /*submitButton.attr("disabled", true);
            alert("Update Successful");*/




       },
       err : function(errData){
         console.log("error");

       }

     });




  });
})
