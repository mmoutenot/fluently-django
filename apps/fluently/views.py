from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User, Group
from django.template import Context
from django.core.context_processors import csrf
from django.template.loader import get_template
from apps.fluently.models import UserProfile, StudentRequest
from utils import mandrill_template
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
import string
from random import choice
import uuid
import sys
import time
import os
import requests
import json
import collections

# Display splash page
def splash(request):
    return render(request, 'fluently/marketing_site/splash.html')

# Display signin page  
def signin(request):
    return render(request, 'fluently/app_site/sign-in.html')

# Display about page  
def about(request):
    return render(request, 'fluently/marketing_site/about.html')

# Display how it works page  
def how_it_works(request):
    return render(request, 'fluently/marketing_site/how-it-works.html')

# Display privacy policy page
def privacy(request):
    return render(request, 'fluently/marketing_site/privacy.html')

# Check validity of signin info from client via request
# Redirect to space or send error
def handle_sign_in(request):
    email = password = ''
    response_json = {"status": "fail"}
    if request.POST:
        email = request.POST.get('signin_email')
        password = request.POST.get('signin_password')
        print 'trying to log in with ', email, password
        user = authenticate(username=email, password=password)
        print user
        if user is not None:
            login(request, user)
            return redirect('/fluently/public_profile/public_profile.html')
            print 'user logged in'
        else:
            print 'invalid user'
            error_msg = "Invalid username or password. Please try again."
            template = get_template('fluently/sign_in.html')
            context = Context({"error_msg": error_msg})
            context.update(csrf(request))
            return HttpResponse(template.render(context))
    else:
        return HttpResponse(json.dumps(response_json), 
                            mimetype="application/json") 

# Display provider sign up page
def provider_sign_up(request):
    return render(request, 'face/provider-signup.html')

# Request with new student info from register page 
# Save student in database, send emails to CEO and student 
def student_account_handler(request):
    response_json = {"status": "fail"}
    if request.POST:
        email = request.POST.get('email', "")
        name = request.POST.get('name', "")
        location = request.POST.get('loc', "")
        needs = request.POST.get('needs', "")
        print email
        print name
        if StudentRequest.objects.filter(email=email).count():
            response_json = {
                "status": "success",
                "emailed": True
            }
        else:
            r = StudentRequest.objects.create(email=email)
            r.requestType = 'G'
            r.name = name
            r.location = location
            r.needs = needs        
            r.save()
            mandrill_url = ("https://mandrillapp.com/api/1.0/messages/"
                            "send-template.json")
            template_content_ceo = [
                { "name": "name", "content": name },
                { "name": "email", "content": email },
                { "name": "location", "content": location },
                { "name": "needs", "content": needs }]
            mandrill_template_ceo = mandrill_template("student-request", 
                                                      template_content_ceo, 
                                                      "team@fluentlynow.com", 
                                                      "Jack McDermott", 
                                                      "student-request")
            requests.post(mandrill_url, data=mandrill_template_ceo)
            template_content_user = [
                {"name": "name", "content": name }]
            mandrill_template_user = mandrill_template("student-app-received",
                                                   template_content_user,
                                                   email,
                                                   name,
                                                   "student-app-received")
            requests.post(mandrill_url, data=mandrill_template_user) 
            response_json = { 
                "status": "success",
                "emailed": False
            }
    return HttpResponse(json.dumps(response_json), mimetype="application/json") 

# Display register student page
def register_student(request):
    return render(request, 'face/register_student_modal.html')

# Display register student blocks
def register_student_blocks(request):
    return render(request, 'face/register_student_blocks.html')

# Display provider sign up blocks
def provider_sign_up_blocks(request):
    return render(request, 'fluently/app_site/provider_signup/provider_sign_up_blocks.html')

# Display confirm password page
def confirm(request):
    return render(request, 'face/confirm.html')

# Display confirm blocks
def confirm_blocks(request):
    return render(request, 'face/confirm_blocks.html')

# Request with user's join id
# Response with matching user's email if unconfirmed or redirect to signin
def confirm_user(request):
    response_json = {"status": "fail"}
    if request.POST:
        join_id = request.POST.get('join_id', "")
        try: 
            print "here"
            u = UserProfile.objects.filter(join_id=join_id)[0].user
            email = u.username
            confirmed = u.userprofile.confirmed
            response_json = {
                "status": "success", 
                "confirmed": confirmed, 
                "email": email }
            print response_json
            return HttpResponse(json.dumps(response_json), 
                   mimetype="application/json") 
        except:  
            return HttpResponse(json.dumps(response_json), 
                   mimetype="application/json") 
    else:
        return HttpResponse(json.dumps(response_json),
               mimetype="application/json")

# Request with email and password
# Set user's password, login and redirect to space
def confirm_password(request):
    response_json = {"status": "fail"}
    if request.POST:
        email = request.POST.get('email', "")
        password = request.POST.get('password', "")
        if User.objects.filter(username=email).count():
            u = User.objects.filter(username=email)[0]
            u.set_password(password)
            u.userprofile.confirmed = True
            u.save()
            u.userprofile.save()
            u = authenticate(username=email, password=password)
            login(request, u)
            response_json = {"status": "success"}
    return HttpResponse(json.dumps(response_json), mimetype="application/json")
        
# Request with email
# Response with whether matching user has been sent a join email
def register_emailed(request):
    response_json = {"status": "fail"}
    if request.POST:
        email = request.POST.get('email', "")
        if User.objects.filter(username=email).count():
            response_json = {
                "status": "success",
                "emailed": User.objects.filter(username=email)[0]
                           .userprofile.emailed
            }
        else:
            response_json = { 
                "status": "success",
                "emailed": False
            }
    print json.dumps(response_json)
    return HttpResponse(json.dumps(response_json), mimetype="application/json") 

# Request with new user info from register page 
# Save user in database, send emails to CEO and user 
def register_account_handler(request):
    print "handling"
    response_json = {"status": "fail"}
    if request.POST:
        print request.POST
        firstName = request.POST.get('firstName', "")
        lastName = request.POST.get('lastName', "")
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        location = request.POST.get('loc', "")
        specialties = request.POST.get('specialties', "")
        u, created = User.objects.get_or_create(username=email)
        print "created"
        u.set_unusable_password()
        u.userprofile.user_type = 'P'
        alphnum = string.ascii_uppercase + string.digits
        u.userprofile.user_url = ''.join(choice(alphnum) for x in range(6))
        u.userprofile.join_id = str(uuid.uuid1())
        joinlink = 'http://fluentlynow.com/face/confirm?id='
        joinlink = joinlink + u.userprofile.join_id
        u.userprofile.first_name = firstName
        u.userprofile.last_name = lastName
        u.userprofile.phone = phone
        u.userprofile.location = location 
        u.userprofile.specialties = specialties
        u.userprofile.pic_url = "/static/images/default_profile.jpg"
        u.userprofile.emailed = True
        u.save()
        u.userprofile.save()
        mandrill_url = ("https://mandrillapp.com/api/1.0/messages/"
                       "send-template.json")
        template_content_ceo = [
            { "name": "firstName", "content": firstName },
            { "name": "lastName", "content": lastName },
            { "name": "email", "content": email },
            { "name": "phone", "content": phone },
            { "name": "location", "content": location },
            { "name": "specialties", "content": specialties },
            { "name": "joinlink", "content": joinlink}]
        mandrill_template_ceo = mandrill_template("provider-request", 
                                                  template_content_ceo, 
                                                  "team@fluentlynow.com", 
                                                  "Jack McDermott", 
                                                  "provider-request")
        requests.post(mandrill_url, data=mandrill_template_ceo)
        template_content_user = [
            {"name": "firstName", "content": firstName }]
        mandrill_template_user = mandrill_template("provider-app-received",
                                                   template_content_user,
                                                   email,
                                                   firstName,
                                                   "provider-app-received")
        requests.post(mandrill_url, data=mandrill_template_user) 
        response_json = {"status": "success"}
    return HttpResponse(json.dumps(response_json), mimetype="application/json")

def usersContextList():
    keyorder = {k:v for v,k in enumerate(
        ['id', 'name', 'email', 'phone', 'location', 'specialties']
    )}
    users = User.objects.all()
    usersContextList = []
    for user in users:
        userDict = {}
        userDict['specialties'] = user.userprofile.specialties
        userDict['location'] = user.userprofile.location
        userDict['phone'] = user.userprofile.phone
        userDict['email'] = user.username
        userDict['name'] = user.userprofile.name
        userDict['id'] = user.pk
        dictItems = sorted(userDict.items(), key=lambda i:keyorder.get(i[0]))
        userDict = collections.OrderedDict(dictItems)
        usersContextList.append(userDict)
    return usersContextList

def save_profile(request):
    u = request.user
    print u
    if not u.is_authenticated():
        return redirect('/face/')
    response_json = {
        "status": "fail",
    }
    if request.POST:
        print "post save"
        firstName = request.POST.get('firstName', "")
        lastName = request.POST.get('lastName', "")
        location = request.POST.get('loc', "")
        aboutMe = request.POST.get('aboutMe', "")
        certifications = request.POST.get('certifications', "")
        experience = request.POST.get('experience', "")
        therapyApproach = request.POST.get('therapyApproach', "")
        u.userprofile.first_name = firstName
        u.userprofile.last_name = lastName
        u.userprofile.location = location
        u.userprofile.about_me = aboutMe
        u.userprofile.certifications = certifications
        u.userprofile.experience = experience
        u.userprofile.therapy_approach = therapyApproach
        u.userprofile.save()
        print firstName
        print lastName
        print aboutMe
        print location
        print certifications
        print experience
        print therapyApproach
        response_json = {   
            "status": "success",
        }
    return HttpResponse(json.dumps(response_json), mimetype="application/json")

def public_profile(request, user_url):
    print "pub"
    try:
        u = UserProfile.objects.filter(user_url=user_url)[0].user  
        template = get_template('space/public_profile.html')
        firstName = u.userprofile.first_name
        lastName = u.userprofile.last_name
        location = u.userprofile.location
        aboutMe = u.userprofile.about_me
        certifications = u.userprofile.certifications
        experience = u.userprofile.experience
        therapyApproach = u.userprofile.therapy_approach
        userUrl = u.userprofile.user_url
        context = Context({
            "firstName": firstName,
            "lastName": lastName,
            "location": location,
            "aboutMe": aboutMe,
            "certifications": certifications,
            "experience": experience,
            "therapyApproach": therapyApproach,
            "userUrl": userUrl
        })
        print aboutMe
        context.update(csrf(request))
        return HttpResponse(template.render(context))
    except:
        return redirect('/face/')

def contact_student_blocks(request):
    return render(request, 'space/contact_student_blocks.html')

def contact(request, user_url):
    try:
        u = UserProfile.objects.filter(user_url=user_url)[0].user
        template = get_template('space/contact_student_modal.html')
        firstName = u.userprofile.first_name
        lastName = u.userprofile.last_name
        slp = u.username
        print firstName
        print lastName
        context = Context({
            "firstName": firstName,
            "lastName": lastName,
            "slp": slp
        })
        context.update(csrf(request))
        return HttpResponse(template.render(context))
    except:
        return redirect('/face/')

def contact_SLP(request):
    response_json = {"status": "fail"}
    if request.POST:
        email = request.POST.get('email', "")
        name = request.POST.get('name', "")
        location = request.POST.get('loc', "")
        needs = request.POST.get('needs', "")
        slp = request.POST.get('slp', "")
        if StudentRequest.objects.filter(email=email, slp=slp).count():
            response_json = {
                "status": "success",
                "emailed": True
            }
        else:
            r = StudentRequest.objects.create(email=email)
            r.name = name
            r.location = location
            r.needs = needs
            r.slp = slp
            r.requestType = 'S'
            r.save()
            mandrill_url = ("https://mandrillapp.com/api/1.0/messages/"
                            "send-template.json")
            template_content_ceo = [
                { "name": "name", "content": name },
                { "name": "email", "content": email },
                { "name": "location", "content": location },
                { "name": "needs", "content": needs}, 
                { "name": "slp", "content": slp }]
            mandrill_template_ceo = mandrill_template("student-SLP-request", 
                                                      template_content_ceo, 
                                                      "dylan@fluentlynow.com", 
                                                      "Jack McDermott", 
                                                      "student-SLP-request")
            requests.post(mandrill_url, data=mandrill_template_ceo)
            template_content_user = [
                {"name": "name", "content": name }]
            mandrill_template_user = mandrill_template("student-app-received",
                                                   template_content_user,
                                                   email,
                                                   name,
                                                   "student-app-received")
            requests.post(mandrill_url, data=mandrill_template_user) 
            response_json = { 
                "status": "success",
                "emailed": False
            }
    return HttpResponse(json.dumps(response_json), mimetype="application/json") 

def profile(request):
    u = request.user
    template = get_template('space/profile.html')
    if not u.is_authenticated():
        return redirect('/face/')
    if u.username == "jack@fluentlynow.com":
        print "CEO will get..."
        context = Context({
            "users": usersContextList()
        })
        context.update(csrf(request))
        return HttpResponse(template.render(context))
    firstName = u.userprofile.first_name
    lastName = u.userprofile.last_name
    location = u.userprofile.location
    aboutMe = u.userprofile.about_me
    certifications = u.userprofile.certifications
    experience = u.userprofile.experience
    therapyApproach = u.userprofile.therapy_approach
    userUrl = u.userprofile.user_url
    context = Context({
        "firstName": firstName,
        "lastName": lastName,
        "location": location,
        "aboutMe": aboutMe,
        "certifications": certifications,
        "experience": experience,
        "therapyApproach": therapyApproach,
        "userUrl": userUrl
    })
    context.update(csrf(request))
    return HttpResponse(template.render(context))

def profile_picture(request):
    print "profile picture"
    response_json = {"status": "fail"}
    u = request.user
    if request.POST:
        pic_url = request.POST.get('pic_url', "")
        if pic_url:
            u.userprofile.pic_url = pic_url
            u.userprofile.save()
            response_json = {"status": "success"}
        else:
            response_json = {"status": "success", 
                             "pic_url": u.userprofile.pic_url}
    return HttpResponse(json.dumps(response_json), mimetype="application/json")

def account(request):
  u = request.user
  if not u.is_authenticated():
    return redirect('/')
  if not u.userprofile.confirmed:
    return render(request, 'space/unconfirmed.html')
  else:
    try:
      other_users = Group.objects.get(name=u.userprofile.company).user_set.exclude(username=u.username)
      active_users = other_users.filter(userprofile__confirmed=True)
      invited_users = other_users.filter(userprofile__confirmed=False)
      active_usernames = [n[0] for n in active_users.values_list('username')]
      invited_usernames = [n[0] for n in invited_users.values_list('username')]
      print "printing active and invited"
      print active_usernames
      print invited_usernames
      template = get_template('space/account.html')
      context = Context({"invited_users":invited_users})
      context.update(csrf(request))
      return HttpResponse(template.render(context))
    except:
      return render(request, 'space/account.html')

