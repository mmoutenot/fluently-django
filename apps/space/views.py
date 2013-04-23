from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods

import uuid

from vendor.TokBox import OpenTokSDK

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

@require_http_methods(["GET"])
def dispatch(request):
  print 'in dispatch'
  s = Space(tok_session_id = TokBox.generate_session_id(), url_id=uuid.uuid4())
  s.save()

  return redirect('/%s' % str(s.url_id))

@require_http_methods(["GET"])
def main(request, space_url_id):
  print 'in main'
  s = get_object_or_404(Space, url_id=space_url_id)
  tok_token = TokBox.generate_token(s.tok_session_id)
  return render(request, 'space/index.html',
                {
                  "space":s,
                  "tok_token":tok_token,
                  "tok_session_id":s.tok_session_id
                })


