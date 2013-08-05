$(document).ready(function () {   

  $.ajax({
    type: "post",
    dataType: "json",
    url: "/account-edit/handler/",
    data: data,
    success: function(dataJSON) {
      if (!dataJSON['viewed']) {
        console.log('sup');
        $('#myModal').modal('show');  
      }
    }
  });

  // Spin animation

  var opts = {
    lines: 9,
    length: 0,
    width: 8,
    radius: 10,
    corners: 1,
    color: '#ffffff'
  };

  $.ajax({
    type: "post",
    dataType: "json",
    url: "/account-edit/handler/",
    data: {csrfmiddlewaretoken: csrf_token},
    success: function(dataJSON) {
      if (!dataJSON['viewed']) {
        $('#welcome-blocks-wrapper').load(
          '/account-edit/blocks #welcome-block');
      } else {
        $('#welcome-blocks-wrapper').load(
          '/account-edit/blocks #edit-specialties-block',
          function () {
            console.log('ello');
            $('#select-to').prop('selectedIndex', -1);
            $('#select-to').selectize({
              maxItems: 6,
              hideSelected: true
            });
            $('#select-to1').selectize({
              hideSelected: true,
              maxItems: 5,
            });
          }
        );
      }
    }
  });

  $('#welcome-form').live('submit', function () {
    console.log('what');
    $('#welcome-blocks-wrapper').load(
      '/account-edit/blocks #edit-specialties-block',
      function () {
          console.log('ello');
          $('#select-to').prop('selectedIndex', -1);
          $('#select-to').selectize({
            maxItems: 6,
            hideSelected: true
          });
          $('#select-to1').selectize({
            hideSelected: true,
            maxItems: 5,
          });
        }); 
      });
    return false;
  });

  $('#edit-specialties-form').live('submit', function () {
    console.log('edit submit');

    certs = []; 
    $('#select-to1 option').each(
      function () {
        certs.push($(this).val());
      }
    ); 

    specs = [];
    $('#select-to option').each(
      function () {
        specs.push($(this).val());
      }
    ); 
  
    formData = {
      city: $('#city-input').val(),
      state: $('#state-input').val(),
      certifications: certs.toString(),
      specialties: specs.toString(),
      csrfmiddlewaretoken: csrf_token
    };

    console.log(formData);

    $.ajax({
      type: "post",
      dataType: "json",
      url: "/account-edit/options-handler-1/",
      data: formData,
      success: function(dataJSON) {
        console.log('1st page to server');
      }
    });

    $('#welcome-blocks-wrapper').load(
        '/account-edit/blocks #edit-advanced-specialties-block');
    return false;
  });

  $('#edit-advanced-specialties-form').live('submit', function () {

    ages = [];
    $('.age').each(
      function () {
        if ($(this).is(':checked')) {
          ages.push($(this).val());
        }
      }
    );
    if (ages[0] == 'all') {
      ages.splice(0, 1);
    } 

    locs = [];
    $('.loc').each(
      function() {
        if ($(this).is(':checked')) {
          locs.push($(this).val());
        }
      }
    ); 

    pays = [];
    $('.pay').each(
      function() {
        if ($(this).is(':checked')) {
          pays.push($(this).val());
        }
      }
    ); 
 
    formData = {
      age: ages.toString(),
      loc: locs.toString(),
      pay: pays.toString(),
      csrfmiddlewaretoken: csrf_token
    };
    
    $.ajax({
      type: "post",
      dataType: "json",
      url: "/account-edit/options-handler-2/",
      data: formData,
      success: function(dataJSON) {
        console.log('2nd page to server');
      }
    });

  });

  $('#select-all').live('click', function () {
    $('.age').prop('checked', $('#select-all').is(':checked'));
  });

});


