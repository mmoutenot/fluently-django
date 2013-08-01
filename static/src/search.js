$('#search-button').live('click', function () {

    console.log('find');

    searchData = {
      need: $('#select-need').find(':selected').val(),
      zipCode: $('#zip-code').val(),
      locatedIn: $('#located-in').val(),
      payment: $('#payment').val(),
      csrfmiddlewaretoken: csrf_token
    };

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/search/search-results/",
      data: searchData,
      success: function (dataJSON) {    
        console.log(dataJSON);
      }
    });
  
});
