# django libraries
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods

# general python packages
import uuid
import sys
import time
import os

# third party packages
from vendor.TokBox import OpenTokSDK
import crocodoc
from crocodoc import CrocodocError

# models
from models import Space

class TokBox:

  api_key = '25204042' # Replace with your OpenTok API key.
  api_secret = '28ae8c58d5b4e013841581e5cd26df2c9851a818' # Replace with your OpenTok API secret.
  session_address = 'http://localhost:8000' # Replace with the representative URL of your session.

  @classmethod
  def generate_session_id(self):
    opentok_sdk = OpenTokSDK.OpenTokSDK(self.api_key, self.api_secret)
    session = opentok_sdk.create_session(self.session_address)
    print 'created session: ' + session.session_id
    return session.session_id

  @classmethod
  def generate_token(self, session_id):
    opentok_sdk = OpenTokSDK.OpenTokSDK(self.api_key, self.api_secret)
    connectionMetadata = ''
    token = opentok_sdk.generate_token(session_id, OpenTokSDK.RoleConstants.PUBLISHER, None, connectionMetadata)
    print 'created token: ' + token
    return token

class Crocodoc:
  c = crocodoc
  c.api_token = 'Tw6f4QKEneJ8qiHzCRL7bOlF'

  @classmethod
  def upload(self, file_handle):
    sys.stdout.write('  Uploading... ')
    uuid = None
    try:
      uuid = self.c.document.upload(file=file_handle)
      print '  UUID is ' + uuid
      return uuid
    except CrocodocError as e:
      print '  Error Code: ' + str(e.status_code)
      print '  Error Message: ' + e.error_message
      return None

  @classmethod
  def generate_session_id(self, uuid):
    try:
      session_id = self.c.session.create(uuid)
      print '  session is ' + session_id
      return session_id
    except CrocodocError as e:
      print '  Error Code: ' + str(e.status_code)
      print '  Error Message: ' + e.error_message
      return None

@require_http_methods(["GET"])
def dispatch(request):
  print 'in dispatch'
  s = Space(tok_session_id = TokBox.generate_session_id(), url_id=uuid.uuid4())
  s.save()

  return redirect('/space/%s/' % str(s.url_id))

@require_http_methods(["GET"])
def main(request, space_url_id):
  print 'in main'
  s = get_object_or_404(Space, url_id=space_url_id)

  tok_token = TokBox.generate_token(s.tok_session_id)
  tok_token=None

  return render(request, 'space/index.html',
                {
                  "space"          : s,
                  "tok_token"      : tok_token,
                  "tok_session_id" : s.tok_session_id,
                  "croco_session"  : s.croco_session
                })

@require_http_methods(["GET","POST"])
def upload(request):
  print 'in upload view'
  print request.FILES

  space_id = request.POST.get('space_id')
  space = Space.objects.get(id=space_id)

  croco_uuid = handle_uploaded_file(request.FILES['file'])
  croco_session = Crocodoc.generate_session_id(croco_uuid)

  space.croco_session = croco_session
  space.save()

  return HttpResponse(croco_session)

def handle_uploaded_file(f):
  croco_session = None
  try:
    croco_uuid = Crocodoc.upload(f)
  except CrocodocError as e:
    print '  Error Code: ' + str(e.status_code)
    print '  Error Message: ' + e.error_message
    return None
  return croco_uuid

