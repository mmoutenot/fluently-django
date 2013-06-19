$(document).ready(function() {

  $('.submit').prop('disabled', true);
  observeInterval = 100;
  setInterval(function() { 
    noBlanks = true;
    $('.text_input').each(function() {
      if ($(this).val() == '') {
        noBlanks = false;
      }
    });
    $('.submit').prop('disabled', !noBlanks);
  }, observeInterval);

  $('#invite-user-form').live('submit', function() {
    
    $.ajax({
      type: "post",
      dataType: "json",
      url: "/space/invite_user/",
      data: { 
        email: $('#invite-email').val(),
        csrfmiddlewaretoken: csrf_token 
      },
      success: function(data) {
        dataJSON = jQuery.parseJSON(data);
        if (dataJSON['status'] === "OK") {
          $('#status').text("Successfully invited " + $('#invite-email').val());
          $('#invite-email').val("");
        } else if (dataJSON['status'] === "DUP") {
          $('#status').text("User has already been invited.");
          $('#invite-email').val("");
        }
      }
    });

    return false;
    
  });

});
