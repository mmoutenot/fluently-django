from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core.context_processors import csrf
from models import UserProfile
from utils import email_template
import json
import requests
import uuid

"""  
Responses:
  OK - all good, continue to the next step
  INV - email invalid
  DUP - email already taken
"""

def main(request):
  return render(request, 'face/landing.html')

def signin(request):
  return render(request, 'face/signin.html')

def signin_user(request):
  email = password = ''
  if request.POST:
    email = request.POST.get('signin_email')
    password = request.POST.get('signin_password')
    print 'trying to log in with ', email, password
    user = authenticate(username=email, password=password)
    print user
    if user is not None:
      login(request, user)
      print 'user logged in'
      return redirect('/space/')
    else:
      print 'invalid user'
      error_msg = "Invalid username or password. Please try again."
      template = get_template('face/signin.html')
      context = Context({"error_msg":error_msg})
      context.update(csrf(request))
      return HttpResponse(template.render(context))
  return render(request, 'face/signin.html')

def register_user(request):
  return render(request, 'face/register.html')

def register_blocks(request):
  return render(request, 'face/register_blocks.html')

def register_emailed(request):
  response_string = '{"status":"OK"}'
  if request.POST:
    email = request.POST.get('email', "")
    if User.objects.filter(username=email).count():
      if User.objects.filter(username=email)[0].userprofile.emailed:
        response_string = '{"status":"DUP"}'
  return HttpResponse(json.dumps(response_string), mimetype="application/json") 
    
def register_account_handler(request):
  response_string = '{"status":"INV"}'
  if request.POST:
    name = request.POST.get('name', "")
    email = request.POST.get('email', "")
    phone = request.POST.get('phone', "")
    state = request.POST.get('company', "")
    specialties = request.POST.get('specialties', "")
    u, created = User.objects.get_or_create(username=email)
    if created:
      u.userprofile.join_id = str(uuid.uuid1())
      u.userprofile.name = name
      u.userprofile.phone = phone
      u.userprofile.state = state
      u.userprofile.specialties = specialties
      u.userprofile.emailed = True
      u.save()
      u.userprofile.save()
      u.userprofile.save()
      template_content = [{ "name": "name", "content": name },
                          { "name": "email", "content": email },
                          { "name": "phone", "content": phone },
                          { "name": "state", "content": state },
                          { "name": "specialties", "content": specialties }]
      mandrill_email_template = email_template("client-request", template_content, "jack@fluentlynow.com", "Jack McDermott", "client-request")
      mandrill_url = "https://mandrillapp.com/api/1.0/messages/send-template.json"
      r = requests.post(mandrill_url, data=mandrill_email_template)
      response_string = '{"status":"OK"}'
  return HttpResponse(json.dumps(response_string), mimetype="application/json")
