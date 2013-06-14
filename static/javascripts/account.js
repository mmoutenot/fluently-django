$(document).ready(function() {

  $.ajax({
    type: "post",
    dataType: "json",
    url: "/space/profile/",
    data: { 
      change: false,
      csrfmiddlewaretoken: csrf_token },
    success: function(data) {
      dataJSON = jQuery.parseJSON(data);
      if (dataJSON['status'] === "OK") {
        $('#first-name').val(dataJSON['firstName']);
        $('#email').val(dataJSON['email']);
      }
    }
  });

  $('body').click(function() {
    $('#status').text("");
  });

  $('.user-field').change(function() {
    
    $('#status').text("ALL YOUR INFORMATION HAS BEEN PROCESSED AND YOU BELONG TO US NOW");  

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/space/profile/",
      data: { 
        change: true,
        firstName: $('#first-name').val(),
        email: $('#email').val(),
        csrfmiddlewaretoken: csrf_token 
      },
      success: function(data) {
        dataJSON = jQuery.parseJSON(data);
        if (dataJSON['status'] === "OK") {
          $('#name').text(dataJSON['name']);
          $('#email').text(dataJSON['email']);
        }
      }
    });

  });

});
