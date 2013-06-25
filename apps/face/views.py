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

# Display register blocks
def register_blocks(request):
    return render(request, 'face/register_blocks.html')

# Request with user's join id
# Response with matching user's confirmation status and with email if confirmed
def register_confirmed(request):
    response_json = {"status": "fail"}
    if request.POST:
        join_id = request.POST.get('join_id', "")
        try: 
            u = UserProfile.objects.filter(join_id=join_id).user
            email = UserProfile.objects.filter(join_id=join_id).user.username
            response_json = {
                "status": "success", 
                "confirmed": u.userprofile.confirmed, 
                "email": email }
        except:  
            pass
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
    return HttpResponse(json.dumps(response_json), mimetype="application/json") 

# Request with new user info from register page 
# Save user in database, send email to CEO 
def register_account_handler(request):
    response_json = '{"status":"INV"}'
    if request.POST:
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        state = request.POST.get('state', "")
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
            template_content_ceo = [
                { "name": "name", "content": name },
                { "name": "email", "content": email },
                { "name": "phone", "content": phone },
                { "name": "state", "content": state },
                { "name": "specialties", "content": specialties }]
            mandrill_template_ceo = mandrill_template("provider-request", 
                                                      template_content_ceo, 
                                                      "dylan@fluentlynow.com", 
                                                      "Jack McDermott", 
                                                      "provider-request")
            mandrill_url = """https://mandrillapp.com/api/1.0/messages/
                           send-template.json"""
            requests.post(mandrill_url, data=mandrill_template_ceo)
            response_json = '{"status":"OK"}'
    return HttpResponse(json.dumps(response_json), mimetype="application/json")
