$(document).ready(function() {
  $(".add-friend-button").on('click', function(event){
    var to_id = $(event.target).attr("id");
    $.ajax({
      url: "/api/subscribe",
      headers: {'X-CSRFToken': getCookie('csrftoken')
        ,'sessionid':getCookie('sessionid')},
      data: {"from_id": from_id, "to_id": to_id},
      type: "POST",
      success: function(data)
      {
        console.log(data);
        $(`#${to_id}`).html(data["Success"]);
      },
      error: function() {}
    });
  });
});
