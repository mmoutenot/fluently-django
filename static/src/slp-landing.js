$(document).ready(function () {

  observeInterval = 100;
  setInterval(function () {
    firstName = $('#firstName').val();
    email = $('#email').val(); 
    url = "/join?"
    if (firstName) {
      url += "firstName=" + firstName;
      if (email) {
        url += "&email=" + email;
      }
    } else if (email) {
      url += "email=" + email;
    }
    $('#complete-free-profile').attr('href', url);
  }, observeInterval);

	$('.ebook-button').click(function () {

    $.ajax({
      type: 'post',
      dataType: 'json',
      url: '/ebook/',
      data: {
        recipientType: 'slp',
        email: $('#signin_email').val(),
        csrfmiddlewaretoken: csrf_token 
      },
      success: function (dataJSON) {
        $('#sent-success').css('visibility', 'visible');
        setTimeout(function () {
          $('#sent-success').css('visibility', 'hidden');
        }, 2000); 
      }
    });

  });

});
    
    
