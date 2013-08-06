function initModalContents() {
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
            $('#select-to').prop('selectedIndex', -1);
            $('#select-to').selectize({
              maxItems: 6,
              hideSelected: true
            });
            $('#select-to1').selectize({
              hideSelected: true,
              maxItems: 5,
            });
            $.ajax({
              type: "post",
              dataType: "json",
              url: "/account-edit/fields-handler-1/",
              data: { csrfmiddlewaretoken: csrf_token},
              success: function (dataJSON) {
                $('#city-input').val(dataJSON.city);
                $('#state-input').val(dataJSON.state);
                $('#select-job').val(dataJSON.role);
                $('#select-to1')[0].selectize.clear();
                for (i in dataJSON.specialties) {
                  $('#select-to')[0].selectize.addItem(
                    dataJSON.specialties[i]);
                }
                for (i in dataJSON.certifications) {
                  $('#select-to1')[0].selectize.addItem(
                    dataJSON.certifications[i]);
                }
                if (!dataJSON.certifications.length) {
                  $('#select-to1')[0].selectize.addItem('ccc');
                }   
                $('#select-to')[0].selectize.close();
                $('#select-to1')[0].selectize.close();
              }
            });
          }
        );
      }
    }
  });
}

function initAdvancedModalContents() {
  $.ajax({
    type: "post",
    dataType: "json",
    url: "/account-edit/fields-handler-2/",
    data: { csrfmiddlewaretoken: csrf_token},
    success: function (dataJSON) {
      for (i in dataJSON.ages) {
        $('input').each(function () {
          if ($(this).val() == dataJSON.ages[i]) {
            $(this).prop('checked', true);
          }
        });
      }
      for (i in dataJSON.locs) {
        $('input').each(function () {
          if ($(this).val() == dataJSON.locs[i]) {
            $(this).prop('checked', true);
          }
        });
      }
      for (i in dataJSON.pays) {
        $('input').each(function () {
          if ($(this).val() == dataJSON.pays[i]) {
            $(this).prop('checked', true);
          }
        });
      }
    }
  });
}

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

  initModalContents();

  $('#modal-link').click(function () {
    initModalContents();  
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
    return false;
  });

  $('#edit-specialties-form').live('submit', function () {
    
    var noBlanks = true;
    $('.text-input').each(function () {
      if ($(this).val() == '') {
        noBlanks = false;
      }
    });
    if (!$('#select-to1 option').length) {
      noBlanks = false;
    }
    if (!$('#select-to option').length) {
      noBlanks = false;
    }  
    if (noBlanks) {

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
        role: $('#select-job option:selected').val(),
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
        '/account-edit/blocks #edit-advanced-specialties-block',
        function () {
          initAdvancedModalContents(); 
        }
      );

    }
    return false;

  });

  $('#edit-advanced-specialties-form').live('submit', function () {

    ageBlank = true;
    locBlank = true;
    payBlank = true;
    $('input:checkbox.age').each(function () {
      if ($(this)[0].checked) {
        ageBlank = false;
      }
    });
    $('input:checkbox.loc').each(function () {
      if ($(this)[0].checked) {
        locBlank = false;
      }
    });
    $('input:checkbox.pay').each(function () {
      if ($(this)[0].checked) {
        payBlank = false;
      }
    });
  
    if (!ageBlank && !locBlank && !payBlank) {

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

      console.log(formData);
      
      $.ajax({
        type: "post",
        dataType: "json",
        url: "/account-edit/options-handler-2/",
        data: formData,
        success: function(dataJSON) {
          $('#myModal').modal('toggle');
        }
      });
      return false; 
    } else {
      return false;
    }

  });

  $('#select-all').live('click', function () {
    $('.age').prop('checked', $('#select-all').is(':checked'));
  });

});


