$(document).ready(function () {
	
  $('.ebook-button').click(function () {

    if (!$('#signin_email').val()) {
      $.ajax({
        type: 'post',
        dataType: 'json',
        url: '/ebook/',
        data: {
          recipientType: 'parent',
          email: $('#signin_email').val(),
          csrfmiddlewaretoken: csrf_token 
        },
        success: function (dataJSON) {
          $('#sent-success').css('visibility', 'visible');
          setTimeout(function () {
            $('#sent-success').css('visibility', 'hidden');
          }, 4000); 
        }
      });
    }

  });

}); 
    
    
