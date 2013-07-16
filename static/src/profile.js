Shadowbox.init({});

// Get profile picture

data = {
    csrfmiddlewaretoken: csrf_token
};

$.ajax({
  type: "post",
  dataType: "json",
  url: "/space/picture/",
  data: data,
  success: function(dataJSON) {
    if (dataJSON['status'] === "success") {
      $('#prof-pic-img').css(
        'background-image', 
        'url("' + dataJSON.pic_url + '")'
      );
    } 
  }
});


