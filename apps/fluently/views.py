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
from django.db.models import Q
from random import choice
import string
import uuid
import sys
import time
import os
import requests
import json
import collections

###               
###               
### TEMPLATE URLS 
###               
###               

# Marketing Site
splash_url = 'fluently/marketing_site/splash.html'
about_url = 'fluently/marketing_site/about.html'
how_it_works_url = 'fluently/marketing_site/how-it-works.html'
privacy_url = 'fluently/marketing_site/privacy.html'
example_profile_url = 'fluently/marketing_site/example-profile.html'
example_consumer_contact_url = 'fluently/marketing_site/example-consumer-contact.html'
example_consumer_contact_blocks_url = 'fluently/marketing_site/example-consumer-contact-blocks.html'
slp_landing_url = 'fluently/marketing_site/slp-landing.html'

# App Site
sign_in_url = 'fluently/app_site/sign-in.html'

# App Site # Search View

search_url = 'fluently/app_site/search_view/search.html'
profile_card_url = 'fluently/app_site/search_view/profile-card.html'
no_results_url = 'fluently/app_site/search_view/no-results.html'

# App Site # Provider Signup
provider_sign_up_url = 'fluently/app_site/provider_signup/provider-sign-up.html'
provider_sign_up_blocks_url = 'fluently/app_site/provider_signup/provider-sign-up-blocks.html'
provider_confirm_url = 'fluently/app_site/provider_signup/provider-confirm.html'
provider_confirm_blocks_url = 'fluently/app_site/provider_signup/provider-confirm-blocks.html'
provider_confirm_url_prefix = 'http://fluentlynow.com/confirm?id='

# App Site # Consumer Request
consumer_request_url = 'fluently/app_site/consumer_request/consumer-request.html'
consumer_request_blocks_url = 'fluently/app_site/consumer_request/consumer-request-blocks.html'

# App Site # Personal Account
account_url = 'fluently/app_site/personal_account/account.html'
default_profile_pic_url = '/static/images/elements/default-profile.jpg'

# App Site # Public Profile
public_profile_url = 'fluently/app_site/public_profile/public-profile.html'

# App Site # Public Profile # Consumer Contact
consumer_contact_url = 'fluently/app_site/public_profile/consumer_contact/consumer-contact.html'
consumer_contact_blocks_url = 'fluently/app_site/public_profile/consumer_contact/consumer-contact-blocks.html'

###
###                        
### PAGE DISPLAY FUNCTIONS 
###                        
###

# Display splash page
def splash(request):
    return render(request, splash_url)

# Display signin page  
def sign_in(request):
    return render(request, sign_in_url)

# Display about page  
def about(request):
    return render(request, about_url)

# Display how it works page  
def how_it_works(request):
    return render(request, how_it_works_url)

# Display privacy policy page
def privacy(request):
    return render(request, privacy_url)

# Display example profile page
def example_profile(request):
    return render(request, example_profile_url)

# Display example consumer contact page
def example_consumer_contact(request):
    return render(request, example_consumer_contact_url)

# Display example consumer contact blocks page
def example_consumer_contact_blocks(request):
    return render(request, example_consumer_contact_blocks_url)

# Display SLP landing page
def slp_landing(request):
    return render(request, slp_landing_url)

# Display search page
def search(request):
    return render(request, search_url)

# Display profile card block
def profile_card(request):
    return render(request, profile_card_url)

# Display no results block
def no_results(request):
    return render(request, no_results_url)

# Display provider sign up page
def provider_sign_up(request):
    firstName = request.GET.get('firstName')
    email = request.GET.get('email')
    return render(request, provider_sign_up_url)

# Display consumer request modal page
def consumer_request(request):
    return render(request, consumer_request_url)

# Display consumer request blocks
def consumer_request_blocks(request):
    return render(request, consumer_request_blocks_url)

# Display provider sign up blocks
def provider_sign_up_blocks(request):
    return render(request, provider_sign_up_blocks_url)

# Display provider confirm password page
def provider_confirm(request):
    return render(request, provider_confirm_url)

# Display provider confirm blocks
def provider_confirm_blocks(request):
    return render(request, provider_confirm_blocks_url)

# Display account page
def account(request):
    u = request.user
    template = get_template(account_url)
    if not u.is_authenticated():
        return redirect('/')
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

# Display consumer contact blocks
def consumer_contact_blocks(request, user_url):
    return render(request, consumer_contact_blocks_url)

# Display consumer contact page
def consumer_contact(request, user_url):
#   try:
    u = UserProfile.objects.filter(user_url=user_url)[0].user
    template = get_template(consumer_contact_url)
    firstName = u.userprofile.first_name
    lastName = u.userprofile.last_name
    slp = u.username
    print firstName
    print lastName
    context = Context({
        "firstName": firstName,
        "lastName": lastName[0] + '.',
        "slp": slp
    })
    context.update(csrf(request))
    return HttpResponse(template.render(context))
#    except:
#        return redirect('/')

# Display public profile page for provider based on given url
def public_profile(request, user_url):
    print "pub"
    try:
        u = UserProfile.objects.filter(user_url=user_url)[0].user  
        template = get_template(public_profile_url)
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
            "lastName": lastName[0] + '.',
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
        return redirect('/')

###        
###          
### HANDLERS 
###          
###

def search_results(request):
    response_json = {"status": "fail"}
    if request.POST:
        need = request.POST.get('need', '')
        zipCode = request.POST.get('zipCode', '')
        locatedIn = request.POST.get('locatedIn', '')
        payment = request.POST.get('payment', '')
        
    return HttpResponse(json.dumps(response_json),
                        mimetype='application/json')

# Check validity of sign in info from client via request
# Redirect to account or send error
def sign_in_handler(request):
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
            return redirect(account_url)
            print 'user logged in'
        else:
            print 'invalid user'
            error_msg = "Invalid username or password. Please try again."
            template = get_template(sign_in_url)
            context = Context({"error_msg": error_msg})
            context.update(csrf(request))
            return HttpResponse(template.render(context))
    else:
        return HttpResponse(json.dumps(response_json), 
                            mimetype="application/json") 

# Request with new consumer info from consumer request page 
# Save consumer in database, send emails to CEO and consumer 
def consumer_request_handler(request):
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

# Request with provider's join id
# Response with matching user's email if unconfirmed or redirect to sign in
def provider_confirm_id(request):
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
# Set provider's password, login and redirect to space
def provider_confirm_password(request):
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
# Response with whether matching provider has been sent a join email
def provider_sign_up_emailed(request):
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

# Request with new provider info from sign up page 
# Save provider in database, send emails to CEO and provider 
def provider_sign_up_handler(request):
    print "handling"
    response_json = {"status": "fail"}
    if request.POST:
        print request.POST
        firstName = request.POST.get('firstName', "")
        lastName = request.POST.get('lastName', "")
        email = request.POST.get('email', "")
        phone = request.POST.get('phone', "")
        zipCode = request.POST.get('zipCode', "")
        country = request.POST.get('country', "")
        specialties = request.POST.get('specialties', "")
        u, created = User.objects.get_or_create(username=email)
        print "created"
        u.set_unusable_password()
        u.userprofile.user_type = 'P'
        alphnum = string.ascii_uppercase + string.digits
        u.userprofile.user_url = ''.join(choice(alphnum) for x in range(6))
        u.userprofile.join_id = str(uuid.uuid1())
        provider_confirm_link = provider_confirm_url_prefix + u.userprofile.join_id
        u.userprofile.first_name = firstName
        u.userprofile.last_name = lastName
        u.userprofile.phone = phone
        u.userprofile.zip_code = zipCode
        u.userprofile.country = country
        u.userprofile.specialties = specialties
        u.userprofile.pic_url = default_profile_pic_url
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
            { "name": "zipCode", "content": zipCode },
            { "name": "country", "content": country },
            { "name": "specialties", "content": specialties },
            { "name": "joinlink", "content": provider_confirm_link}] 
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

# Get posted provider profile info and save to database
def save_profile(request):
    u = request.user
    print u
    if not u.is_authenticated():
        return redirect('/')
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

# Get posted consumer contact info
# Send emails to CEO and consumer
def consumer_contact_handler(request):
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
                                                      "team@fluentlynow.com", 
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



# Get or update profile picture of logged in provider   
def profile_picture_handler(request):
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
