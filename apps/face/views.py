from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from models import UserProfile
from utils import email_template
import json
import requests
import uuid

def main(request):
  return render(request, 'face/login.html')

def login_user(request):
  email = password = ''
  if request.POST:
    email = request.POST.get('login_email')
    password = request.POST.get('login_password')
    print 'trying to log in with ', email, password
    user = authenticate(username=email, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        print 'user active and logged in!'
        return redirect('/space/')
      else:
       print 'user not active'
    else:
      print 'invalid user'
  return redirect('/')

def register_user(request):
  return render(request, 'face/register.html')

def register_blocks(request):
  return render(request, 'face/register_blocks.html')

"""
Receives ajax call from register page and parses POST to check for validity on
the server side.

Responses:
  OK - all good, continue to the next step
  INV - email invalid
  DUP - email already taken
"""
def register_account_handler(request):
  response_string = '{"status":"INV"}'
  if request.POST:
    stage = request.POST.get('stage', "")   
    if stage == "account":
      first_name = request.POST.get('firstName', "")
      last_name  = request.POST.get('lastName', "")
      email      = request.POST.get('email', "")
      password   = request.POST.get('password', "")
      print email
      u, created = User.objects.get_or_create(username=email)
      if created:
        u.password               = password
        u.userprofile.join_id    = str(uuid.uuid1())
        u.userprofile.first_name = first_name
        u.userprofile.last_name  = last_name
        u.save()
        u.userprofile.save()
        template_content = [{
          "name": "joinlink", 
          "content": "<a href='http://www.fluentlynow.com/face/register?id=" + 
                     u.userprofile.join_id + 
                     "'>http://www.fluentlynow.com/face/register?id=" + 
                     u.userprofile.join_id + 
                     "</a>"
          }]
        mandrill_email_template = email_template("invite-user", template_content, email, first_name + " " + last_name, "")
        mandrill_url = "https://mandrillapp.com/api/1.0/messages/send-template.json"
        r = requests.post(mandrill_url, data=mandrill_email_template)
        response_string = '{"status":"OK"}'
      else:
        response_string = '{"status":"DUP"}'
    elif stage == "confirmation":
      join_id = request.POST.get('join_id', "")
      email = UserProfile.objects.filter(join_id=join_id)[0].user.username
      response_string = '{"status":"OK", "email":"' + email + '"}'
    elif stage == "certification":
      certification          = request.POST.get('certification', "")
      education              = request.POST.get('education', "")
      licensed_states        = request.POST.get('licensedStates', "")
      experience_specialties = request.POST.get('experienceSpecialties', "")
      email                  = request.POST.get('email', "")
      try:
        u = User.objects.get(username = email)
        u.userprofile.certification          = certification
        u.userprofile.education              = education
        u.userprofile.licensed_states        = licensed_states
        u.userprofile.experience_specialties = experience_specialties
        u.userprofile.save()
        mandrill_email_template = email_template("submit-user", [], email, u.userprofile.first_name + " " + u.userprofile.last_name, "")
        mandrill_url = "https://mandrillapp.com/api/1.0/messages/send-template.json"
        r = requests.post(mandrill_url, data=mandrill_email_template)
        response_string = '{"status":"OK"}'
      except User.DoesNotExist:
        pass
  return HttpResponse(json.dumps(response_string), mimetype="application/json")
