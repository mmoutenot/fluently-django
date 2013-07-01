from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.core.context_processors import csrf
from models import UserProfile
from utils import mandrill_template
import json
import requests
import uuid

# Display landing page
def main(request):
    return render(request, 'face/landing.html')

# Display signin page  
def signin(request):
    return render(request, 'face/signin.html')

# Check validity of signin info from client via request
# Redirect to space or send error
def handle_signin(request):
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
            print 'user logged in'
            return redirect('/space/')
        else:
            print 'invalid user'
            error_msg = "Invalid username or password. Please try again."
            template = get_template('face/signin.html')
            context = Context({"error_msg": error_msg})
            context.update(csrf(request))
            return HttpResponse(template.render(context))
    else:
        return HttpResponse(json.dumps(response_json), 
                            mimetype="application/json") 

# Display register page
def register(request):
    return render(request, 'face/register.html')

# Request with new student info from register page 
# Save student in database, send emails to CEO and student 
def student_account_handler(request):
    response_json = {"status": "fail"}
    if request.POST:
        email = request.POST.get('email', "")
        name = request.POST.get('name', "")
        location = request.POST.get('loc', "")
        needs = request.POST.get('needs', "")
        if User.objects.filter(username=email).count():
            response_json = {
                "status": "success",
                "emailed": User.objects.filter(username=email)[0]
                           .userprofile.emailed
            }
        else:
            u, created = User.objects.get_or_create(username=email)
            if created:
                u.set_unusable_password()
                u.userprofile.user_type = 'S'
                u.userprofile.join_id = str(uuid.uuid1())
                u.userprofile.name = name
                u.userprofile.location = location 
                u.userprofile.needs = needs
                u.userprofile.emailed = True
                u.save()
                u.userprofile.save()
                mandrill_url = ("https://mandrillapp.com/api/1.0/messages/"
                                "send-template.json")
                template_content_ceo = [
                    { "name": "name", "content": name },
                    { "name": "email", "content": email },
                    { "name": "location", "content": location },
                    { "name": "needs", "content": needs }]
                mandrill_template_ceo = mandrill_template("student-request", 
                                                          template_content_ceo, 
                                                          "dylan@fluentlynow.com", 
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

# Display register blocks
def register_blocks(request):
    return render(request, 'face/register_blocks.html')

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
        print join_id
        try: 
            u = UserProfile.objects.filter(join_id=join_id)[0].user
            print u
            email = u.username
            confirmed = u.userprofile.confirmed
            print confirmed
            response_json = {
                "status": "success", 
                "confirmed": confirmed, 
                "email": email }
            return HttpResponse(json.dumps(response_json), 
                   mimetype="application/json") 
        except:  
            return HttpResponse(json.dumps(response_json),
                   mimetype="application/json")
    else:
        return redirect('/face/')

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
    response_json = {"status": "fail"}
    if request.POST:
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        location = request.POST.get('loc', "")
        specialties = request.POST.get('specialties', "")
        u, created = User.objects.get_or_create(username=email)
        if created:
            u.set_unusable_password()
            u.userprofile.user_type = 'P'
            u.userprofile.join_id = str(uuid.uuid1())
            u.userprofile.name = name
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
                { "name": "name", "content": name },
                { "name": "email", "content": email },
                { "name": "phone", "content": phone },
                { "name": "location", "content": location },
                { "name": "specialties", "content": specialties }]
            mandrill_template_ceo = mandrill_template("provider-request", 
                                                      template_content_ceo, 
                                                      "dylan@fluentlynow.com", 
                                                      "Jack McDermott", 
                                                      "provider-request")
            requests.post(mandrill_url, data=mandrill_template_ceo)
            template_content_user = [
                {"name": "name", "content": name }]
            mandrill_template_user = mandrill_template("provider-app-received",
                                                       template_content_user,
                                                       email,
                                                       name,
                                                       "provider-app-received")
            requests.post(mandrill_url, data=mandrill_template_user) 
            response_json = {"status": "success"}
    return HttpResponse(json.dumps(response_json), mimetype="application/json")
