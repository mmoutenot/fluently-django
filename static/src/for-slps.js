$(document).ready(function () {

	$('.ebook-button').click(function () {
    console.log('elloooo');
    if ($('#signin_email').val()) {
      console.log('ellloooooadfl');
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
          }, 4000); 
        }
      });
    }

  });

});
    
    
