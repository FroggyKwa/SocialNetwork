var btn_up = document.getElementById("btn-up");
var btn_down = document.getElementById("btn-down");
var next_btn = document.getElementById("next-btn")

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function reaction(elem) {
          let likes = 0;

          elem.classList.remove('unactive');
          if(elem === btn_up) {
              btn_down.classList.add('unactive');
          }
          else {
              btn_up.classList.add('unactive');
          }
          if (next_btn)
            next_btn.classList.remove('d-none');
          // if ((!(btn_up.classList.contains("unactive"))) || (!(btn_down.classList.contains("unactive"))))
      }


$(document).ready(function() {
  $("#btn-up").on('click', function(){
    reaction(btn_up);
    $.ajax({
      url: "/api/post_like",
      headers: {'X-CSRFToken': getCookie('csrftoken')
        ,'sessionid':getCookie('sessionid')},
      data: {"post_id": post_id, "user_id": user_id},
      type: "POST",
      success: function(data)
      {
        $(".like-amount").html(data["rating"]);
      },
      error: function(){}
    });
  });

  $("#btn-down").on('click', function(){
    reaction(btn_down);
    $.ajax({
      url: "/api/post_dislike",
      headers: {'X-CSRFToken': getCookie('csrftoken')
        ,'sessionid':getCookie('sessionid')},
      data: {"post_id": post_id, "user_id": user_id},
      type: "POST",
      success: function(data)
      {
        $(".like-amount").html(data["rating"]);
      },
      error: function(){}
    });
  });
});
