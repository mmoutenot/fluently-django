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

$(document).ready(function () {
	$('.ebook-button').click(function () {
    	$('#sent-success').css('visibility', 'visible');
    	setTimeout(function () {
	    	$('#sent-success').css('visibility', 'hidden');
	    }, 2000); 
    }
} 
    
    
