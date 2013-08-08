Shadowbox.init({});

$(document).ready(function () {
	$('.ebook-button').click(function () {
    	$('#sent-success').css('visibility', 'visible');
    	setTimeout(function () {
	    	$('#sent-success').css('visibility', 'hidden');
	    }, 2000); 
    }
} 
    
    
