from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

from utils import send_email_using_template

import json


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

"""
Receives ajax call from register page and parses POST to check for validiy on
the server side.

Responses:
  OK - all good, continue to the next step
  INV - email invalid
  DUP - email already taken
"""
def register_account_handler(request):
  response_string = '{"status":"INV"}'
  if request.POST:
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')
    email = request.POST.get('email')
    password_a = request.POST.get('password')

    u, created = User.objects.get_or_create(username = email)
    if created:
      u.first_name = first_name
      u.last_name  = last_name
      u.email      = email
      u.password   = password_a
      u.save()
      response_string = '{"status":"OK"}'
    else:
      response_string = '{"status":"DUP"}'
      # send_email_using_template()
  return HttpResponse(json.dumps(response_string), mimetype="application/json")

