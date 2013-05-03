from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django_socketio import events

from models import Space
from views import Crocodoc

@events.on_message(channel='^space-')
def message(request, socket, context, message):

  # space = get_object_or_404(Space, message['space_id'])
  print 'message received', message

  if message['action'] == 'loaded_doc':
    croco_session = Crocodoc.generate_session_id(strip_tags(message['croco_uuid']))
    socket.broadcast_channel({'action':'load_doc', 'croco_session':croco_session})
