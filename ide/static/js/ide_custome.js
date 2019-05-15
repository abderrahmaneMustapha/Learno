$('#vote').click(function(){

/* csrf token setup*/

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

$.ajaxPrefilter(function(options, originalOptions, jqXHR){
    if (options['type'].toLowerCase() === "post" || options['type'].toLowerCase() === "patch"

   || options['type'].toLowerCase() === "delete") {
        jqXHR.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
});

/* end fo csrf token setup */

/* get input from form */

  var type =" "
  var url=""
  var vote_class = $("button[name=vote] i").attr('class');
  check_vote =  vote_class.includes('warning')

  var owner = $("input[name=owner-pk]").val();
  var code = $("input[name=code-pk]").val();
  var vote =  $("input[name=vote-pk]").val();

  if (check_vote === true){
    type = "delete"
    url = "http://127.0.0.1:8000/coding-ground/api-votes/votes/"+vote+"/";
  }else{
     type = "post"
     url ="http://127.0.0.1:8000/coding-ground/api-votes/votes/";
  }


    $.ajax({

          type : type,
          url : url,
          dataType: "json",
          contentType: "application/json",

          data :JSON.stringify(
            {
       "owner": owner,
       "code": code,
            }),


          success: function (data) {
              temp0 = $("button[name=vote] i")
              if (type ==="post" ){
                  temp = $("input[name=vote-pk]")
                  temp.attr('value', data['pk']);              

                  temp0.attr('class', 'fas fa-star text-warning')
              }
              else {
                temp0.attr('class', 'fas fa-star')
              }

          }
      })

})
