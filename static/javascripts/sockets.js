
$(function() {

  var addItem = function(selector, item) {
    var template = $(selector).find('script[type="text/x-jquery-tmpl"]');
    template.tmpl(item).appendTo(selector);
  };

  var addMessage = function(data) {
    var d = new Date();
    var win = $(window), doc = $(window.document);
    var bottom = win.scrollTop() + win.height() == doc.height();
    var h = d.getHours();
    var ampm;
    if (h > 12) {
      h -= 12;
      ampm = " PM";
    } else {
      if (h === 0) {
        h = 12;
      }
      ampm = " AM"
    }

    if (data.action == null){
      data.action = "message";
    }

    if (data.name === user_name){
      data.sender = 'local';
    } else {
      data.sender = 'remote';
    }

    data.time = h + ":" + $.map([d.getMinutes()],
      function(s) {
        s = String(s);
        return (s.length == 1 ? '0' : '') + s;
      }) + ampm;
    addItem('#messages', data);
    if (bottom) {
      window.scrollBy(0, 10000);
    }
  };

  var messaged = function(data) {
    switch (data.action) {

      case 'load_doc':
        console.log("viewing document " + data.croco_session);
        $('#documentViewer').attr('src', 'https://crocodoc.com/view/'+data.croco_session);
        break;

      case 'join':
        data.message='entered the space';
        addMessage(data);
        break;

      case 'message':
        addMessage(data);
        break;

      case 'leave':
        data.message='left the space';
        addMessage(data);
        break;
    }
  };

  var connected = function(){
    console.log('connecting to space-'+space_id+' channel');
    socket.subscribe('space-'+space_id);
    if (user_name !== '') {
      socket.send({space: window.space, action: 'start', name: user_name});
      data = {message:'entered the space'};
      data.name=user_name;
      addMessage(data);
    }
  };

  var disconnected = function() {
    setTimeout(start, 1000);
  };


  var start = function() {
    socket = new io.Socket();
    socket.connect();
    socket.on('connect', connected);
    socket.on('disconnect', disconnected);
    socket.on('message', messaged);
  };

  start();

});
