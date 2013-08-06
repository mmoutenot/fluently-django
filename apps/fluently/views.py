from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User, Group
from django.template import Context
from django.core.context_processors import csrf
from django.template.loader import get_template
from apps.fluently.models import UserProfile, StudentRequest, SearchQuery
from utils import mandrill_template
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.db.models import Q
from random import choice
from providerSearch import *
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
### CHOICES 
###
###

# Role Choices

ROLE_CHOICES = (
    (1, 'slp'),
    (2, 'audiologist'),
)

ROLE_CHOICES_DISPLAY = (
    (1, 'Speech-Language Pathologist'),
    (2, 'Audiologist'),
)

# Certification Choices

CERTIFICATION_CHOICES_DISPLAY = (
    (5, 'CCC-SLP'),
    (4, 'MA'),
    (2, 'MS'),
    (3, 'M.Ed'),
    (1, 'Ph.D'),
    (6, 'BRS-FD'),
    (7, 'BRS-S'),
    (8, 'BRS-CL'),
)

CERTIFICATION_CHOICES = (
    (5, 'ccc'),
    (4, 'marts'),
    (2, 'mscience'),
    (3, 'medu'),
    (1, 'phd'),
    (6, 'fluencydisorders'),
    (7, 'swallowing'),
    (8, 'childlang'),
)

# Therapy Need Choices

SPECIALTY_CHOICES_DISPLAY = (
    (1, 'Articulation'), 
    (2, 'Stuttering'),   
    (3, 'Apraxia of Speech'),
    (4, 'Dysarthria'),
    (5, 'Aphasia'),
    (6, 'Autism-Spectrum Disorder'),
    (7, 'Asperger Syndrome'),
    (8, 'Communication Disorder'),
    (9, 'Dyslexia'),
    (10, 'Augmentative & Alternative Communication (AAC)'),
    (11, 'Accent Modification'),
    (12, 'Developmental Delay'),
    (13, 'Dysphagia'),
    (14, 'Other'),
)

SPECIALTY_CHOICES = (
    (1, 'articulation'), 
    (2, 'stuttering'),   
    (3, 'apraxia'),
    (4, 'dysarthria'),
    (5, 'aphasia'),
    (6, 'autism'),
    (7, 'asperger'),
    (8, 'commdisorder'),
    (9, 'dyslexia'),
    (10, 'aac'),
    (11, 'accent'),
    (12, 'devdelay'),
    (13, 'dysphagia'),
    (14, 'other'),
)

# Age Choices

# 1 - 0-4 - child
# 2 - 5-10 - elementary
# 3 - 11-17 - teen
# 4 - 18-65 - adult
# 5 - 66+ - senior

CLIENT_AGE_CHOICES = (
    (1, 'child'),
    (2, 'elementary'),
    (3, 'teen'),
    (4, 'adult'),
    (5, 'senior'),
)

# Located In Choices

# 1 - No Preference
# 2 - Office or Clinic
# 3 - Home
# 4 - Online or Videoconferencing

LOCATED_IN_CHOICES = (
    (1, 'office'),
    (2, 'home'),
    (3, 'online'),
)

# Payment Method Choices

# 1 - No Preference
# 2 - Hourly Rate (Cash/Credit)
# 3 - Accepts Insurance

PAYMENT_METHOD_CHOICES = (
    (1, 'hourly'),
    (2, 'insurance'),
    (3, 'other'),
)

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
account_edit_url = 'fluently/app_site/personal_account/account-edit.html'
account_edit_blocks_url = 'fluently/app_site/personal_account/account-edit-blocks.html'
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
    template = get_template(search_url)
    providers = []
    if UserProfile.objects:
        for i, u in enumerate(UserProfile.objects.all()):
            print u
            provider = {}
            provider['firstName'] = u.first_name
            provider['lastName'] = u.last_name
            provider['zipCode'] = u.zip_code
            provider['specialtiesList'] = u.specialties_list
            provider['locatedIn'] = u.located_in
            provider['paymentMethod'] = u.payment_method
            providers.append(provider)
        print providers
        context = Context({"providers": providers})
        context.update(csrf(request))
        return HttpResponse(template.render(context))
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
    zipCode = u.userprofile.zip_code
    aboutMe = u.userprofile.about_me
    certifications = u.userprofile.certifications
    experience = u.userprofile.experience
    therapyApproach = u.userprofile.therapy_approach
    userUrl = u.userprofile.user_url
    context = Context({
        "firstName": firstName,
        "lastName": lastName,
        "zipCode": zipCode,
        "aboutMe": aboutMe,
        "certifications": certifications,
        "experience": experience,
        "therapyApproach": therapyApproach,
        "userUrl": userUrl
    })
    print userUrl
    context.update(csrf(request))
    return HttpResponse(template.render(context))

# Display account edit page
def account_edit(request):
    u = request.user
    if not u.is_authenticated():
        return redirect('/')
    template = get_template(account_edit_url)
    context = Context({})
    context.update(csrf(request))
    return HttpResponse(template.render(context))

# Display account edit blocks
def account_edit_blocks(request):
    return render(request, account_edit_blocks_url)

# Display consumer contact blocks
def consumer_contact_blocks(request, user_url):
    print user_url
    return render(request, consumer_contact_blocks_url)

# Display consumer contact page
def consumer_contact(request, user_url):
    u = UserProfile.objects.filter(user_url=user_url)[0].user
    template = get_template(consumer_contact_url)
    firstName = u.userprofile.first_name
    lastName = u.userprofile.last_name
    userUrl = u.userprofile.user_url
    slp = u.username
    context = Context({
        "firstName": firstName,
        "lastName": lastName[0] + '.',
        "slp": slp,
        "userUrl": userUrl
    })
    context.update(csrf(request))
    return HttpResponse(template.render(context))

# Display public profile page for provider based on given url
def public_profile(request, user_url):
    print "pub"
    u = UserProfile.objects.filter(user_url=user_url)[0].user  
    template = get_template(public_profile_url)
    firstName = u.userprofile.first_name
    lastName = u.userprofile.last_name
    aboutMe = u.userprofile.about_me
    city = u.userprofile.city
    state = u.userprofile.state
    slp = u.username
    certificationList = u.userprofile.certification_list
    certifications = u.userprofile.certifications
    specialtiesList = u.userprofile.specialties_list
    experience = u.userprofile.experience
    therapyApproach = u.userprofile.therapy_approach
    userUrl = u.userprofile.user_url
    context = Context({
        "firstName": firstName,
        "lastName": lastName[0] + '.',
        "city": city,
        "state": state,
        "role": "Speech-Language Pathologist",
        "specialtiesList": int_to_string_list_database(
                               specialtiesList, 
                               SPECIALTY_CHOICES,
                               SPECIALTY_CHOICES_DISPLAY),
        "aboutMe": aboutMe,
        "certificationList": int_to_string_list_database(
                                certificationList, 
                                CERTIFICATION_CHOICES,
                                CERTIFICATION_CHOICES_DISPLAY),
        "certifications": certifications,
        "experience": experience,
        "therapyApproach": therapyApproach,
        "slp": slp,
        "userUrl": userUrl
    })
    print specialtiesList
    context.update(csrf(request))
    return HttpResponse(template.render(context))

###        
###          
### HANDLERS AND HELPERS
###          
###

def account_field_handler(request):
    u = request.user
    if not u.is_authenticated():
        return redirect('/')
    specialtyIntStr = u.userprofile.specialties_list.replace('[', '').replace(']', '')
    specialtyInts = [int(x) for x in specialtyIntStr.split(',') if x != '']
    specialtyDict = dict((k, v) for k, v in SPECIALTY_CHOICES)
    specialties = [specialtyDict[s] for s in specialtyInts]
    certIntStr = u.userprofile.certification_list.replace('[', '').replace(']', '')
    certInts = [int(x) for x in certIntStr.split(',') if x != '']
    certDict = dict((k, v) for k, v in CERTIFICATION_CHOICES)
    certs = [certDict[s] for s in certInts]
    response_json = {
        "city": u.userprofile.city,
        "state": u.userprofile.state,
        "role": "slp" if u.userprofile.role == 1 else "audiologist",  
        "specialties": specialties,
        "certifications": certs,
    }
    print response_json
    return HttpResponse(json.dumps(response_json),
                        mimetype="application/json")

def account_advanced_field_handler(request):
    u = request.user
    if not u.is_authenticated():
        return redirect('/')
    print 'in it'
    ageIntStr = u.userprofile.client_ages_list.replace('[', '').replace(']', '')
    ageInts = [int(x) for x in ageIntStr.split(',') if x != '']
    ageDict = dict((k, v) for k, v in CLIENT_AGE_CHOICES)
    ages = [ageDict[s] for s in ageInts]
    locIntStr = u.userprofile.located_in.replace('[', '').replace(']', '')
    locInts = [int(x) for x in locIntStr.split(',') if x != '']
    locDict = dict((k, v) for k, v in LOCATED_IN_CHOICES)
    locs = [locDict[s] for s in locInts]
    payIntStr = u.userprofile.payment_method.replace('[', '').replace(']', '')
    payInts = [int(x) for x in payIntStr.split(',') if x != '']
    payDict = dict((k, v) for k, v in PAYMENT_METHOD_CHOICES)
    pays = [payDict[s] for s in payInts]
    response_json = {
        "ages": ages,
        "locs": locs,
        "pays": pays,
    }
    print response_json
    return HttpResponse(json.dumps(response_json),
                        mimetype="application/json")

def int_to_string_list_database(int_list, choices, choices_display):
    out_str = ""
    int_list = int_list[1:-1].split(',')
    int_list = filter(None, int_list)
    int_list.sort()
    print int_list
    for i in int_list:
        for j, choice in list(choices):
            if int(i) == j:
                for k, choice_display in list(choices_display):
                    if j == k:
                        out_str += choice_display + ", "
    out_str = out_str[:-2]
    return out_str


# Convert string list to int list based on choice tuples in models.py
def string_to_int_list_database(str_list, choices):
    out_ids = '['
    str_list = str_list.split(',')
    for s in str_list:
        for i, choice in list(choices):
            if s == choice:
                out_ids += str(i) + ',' 
    out_ids += ']'
    return out_ids

def account_edit_handler(request):
    u = request.user
    if not u.is_authenticated():
        return redirect('/')
    viewed = u.userprofile.viewed_account
    u.userprofile.viewed_account = True
    u.userprofile.save()
    print viewed
    return HttpResponse(json.dumps({"viewed":viewed}),
                        mimetype="application/json")

def account_options_handler(request):
    u = request.user
    if not u.is_authenticated():
        return redirect('/')
    if request.POST:
        u.userprofile.city = request.POST.get('city', '')
        u.userprofile.state = request.POST.get('state', '')
        u.userprofile.role = 1 if request.POST.get('role', '') == 'slp' else 2
        u.userprofile.certification_list = string_to_int_list_database(
                                   request.POST.get('certifications', ''),
                                   CERTIFICATION_CHOICES) 
        u.userprofile.specialties_list = string_to_int_list_database(
                                 request.POST.get('specialties', ''),
                                 SPECIALTY_CHOICES)
        u.userprofile.save()
        return HttpResponse(json.dumps({"status": "success"}),
                            mimetype='application/json')
    return HttpResponse(json.dumps({"status": "fail"}),
                        mimetype='application/json')

def account_advanced_options_handler(request):
    u = request.user
    if not u.is_authenticated():
        return redirect('/')
    if request.POST:
        print 'hello'
        print request.POST.get('age', '')
        print request.POST.get('loc', '')
        print request.POST.get('pay', '')
        u.userprofile.client_ages_list = string_to_int_list_database(
                                 request.POST.get('age', ''),
                                 CLIENT_AGE_CHOICES) 
        u.userprofile.located_in = string_to_int_list_database(
                           request.POST.get('loc', ''),
                           LOCATED_IN_CHOICES)
        u.userprofile.payment_method = string_to_int_list_database(
                              request.POST.get('pay', ''),
                              PAYMENT_METHOD_CHOICES)
        u.userprofile.save()
        return HttpResponse(json.dumps({"status": "success"}),
                            mimetype='application/json')
    return HttpResponse(json.dumps({"status": "fail"}),
                        mimetype='application/json')

def search_results(request):
    response_json = {"status": "fail"}
    if not len(User.objects.all()):
        sample_therapists()
    if request.POST:
        need = request.POST.get('need', '')
        zipCode = request.POST.get('zipCode', '')
        locatedIn = request.POST.get('locatedIn', '')
        payment = request.POST.get('payment', '')
        print need
        print zipCode
        print locatedIn
        print payment 
        q = SearchQuery.objects.create()
        q.need = need
        q.zip_code = zipCode
        q.located_in = locatedIn
        q.payment_method = payment 
        q.save()
        response_json = {"status": "success"}
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
            return redirect('/account/')
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
        zipCode = request.POST.get('zip', "")
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
            r.zip_code = zipCode
            r.needs = needs        
            r.save()
            mandrill_url = ("https://mandrillapp.com/api/1.0/messages/"
                            "send-template.json")
            template_content_ceo = [
                { "name": "name", "content": name },
                { "name": "email", "content": email },
                { "name": "location", "content": zipCode },
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
        zipCode = request.POST.get('zipCode', "")
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
            r.zip_code = zipCode
            r.needs = needs
            r.slp = slp
            r.requestType = 'S'
            r.save()
            mandrill_url = ("https://mandrillapp.com/api/1.0/messages/"
                            "send-template.json")
            template_content_ceo = [
                { "name": "name", "content": name },
                { "name": "email", "content": email },
                { "name": "location", "content": zipCode },
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
