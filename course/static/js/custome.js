$(document).ready(function(){
    var productForm = $(".form-answer-ajax");
    var submitButton = productForm.closest('form').find(':submit');


    productForm.submit(function(event){
      event.preventDefault();
      console.log(" form is not sending");


      var thisForm = $(this);

      var actionEndpoint = thisForm.attr("action");
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();
       $.ajax({

         url : actionEndpoint,
         method : httpMethod,
         data : formData,

         success : function(data){
             console.log("succes");




         },
         err : function(errData){
           console.log("error");

         }

       });




    });
  });
