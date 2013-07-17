/**
 * Display a list of connected users.
 */
var UserDisplay = (function() {

	var cur_username = null;

	var saveCurrentUser = function(username) {
		if(!username) {
			username = $('.current-user').text();
		}
		var data = {
			'message_type': 'user_update',
			'username': username,
			'board_id': boardId
		};
		cur_username = username;
		socket.send(JSON.stringify(data));
		$.cookie("username", username);
	};

	var checkForUsername = function() {
		if($.cookie("username") !== "") {
			cur_username = $.cookie("username");
		}
	};

	var renderUserDisplay = function(users_connected, current_user) {
		$('#user_list').html("");
		var user_display = $('<ul></ul>');
		$.each(users_connected, function(idx, val) {
			var cur_user = $('<li>' + val + '</li>');
			if(val == current_user) {
				if(cur_username && cur_username !== current_user) {
					cur_user.text(cur_username);
					saveCurrentUser(cur_username);
				}
				cur_user.addClass('current-user');
				cur_user.attr("contenteditable", "true");
				cur_user.bind("blur", function(ev) {
					saveCurrentUser();
				});
			}
			user_display.append(cur_user);
		});
		$('#user_list').append(user_display);
	};

	var render = function(data) {
		renderUserDisplay(data['users_connected'], data['current_user']);
	};

	/* Public interface */
	return {
		render: render,
		checkForUsername: checkForUsername
	};
})();


$(function() {
    var saveBoardTitle = function() {
        var text = $('#pinners').html();
        var data = {
          'message_type': 'board_name_update',
          'name': text,
          'board_id': boardId
        };
        socket.send(JSON.stringify(data));
    };
    $('#pinners').blur(saveBoardTitle);
});
