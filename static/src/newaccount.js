$(document).ready(function() {

  $('#newaccount-link').on('click', function () {
    $.ajax({
      type: "post",
      dataType: "json",
      url: "/newaccount-handler/",
      data: { csrfmiddlewaretoken: csrf_token },
      success: function () {
        $('body').append('<a href="/account/">Account Page</a>');
      }
    });
  });

});
