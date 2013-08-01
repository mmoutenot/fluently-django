from django.contrib.auth.models import User
from apps.fluently.models import UserProfile
from random import choice
import uuid
import string

provider_confirm_url_prefix = 'http://fluentlynow.com/confirm?id='
default_profile_pic_url = '/static/images/elements/default-profile.jpg'

specialties_dict = {
    1:'articulation',
    2:'stuttering',
    3:'apraxia',
    4:'dysarthria',
    5:'aphasia',
    6:'autism',
    7:'asperger',
    8:'commdisorder',
    9:'dyslexia',
    10:'aac',
    11:'accent',
    12:'devdelay',
    13:'dysphagia',
    14:'other'
}

located_in_dict = {
    'N':'no-preference',
    'O':'office',
    'H':'home',
    'V':'video'
}

payment_dict = {
    'N':'no-preference',
    'I':'insurance',
    'H':'hourly'
}

def get_specialties_from_index(i):
    return specialties_dict[i]

def get_specialties_from_index(i):
    return located_in_dict[i]

def get_payment_from_index(i):
    return payment_dict[i]

def sample_therapists():

    index_to_specialties_dict = {
        0:'[13,7,3]',
        1:'[14,5,4,7]',
        2:'[2,11,3]',
        3:'[10,5,6,2]',
        4:'[7,14,8,13]',
        5:'[13,9,6,1]',
        6:'[1,7,2,13]',
        7:'[5,14,6]',
        8:'[10,6,11,3]',
        9:'[8,9,12,10]'
    }
    
    index_to_loc_dict = {
        0:'O',
        1:'H',
        2:'H, V',
        3:'H, O',
        4:'N',
        5:'H, O',
        6:'H, V, O',
        7:'V, O',
        8:'N',
        9:'V, H'
    }

    index_to_payment_dict = {
        0:'H, I',
        1:'N',
        2:'I, H',
        3:'I, H',
        4:'H',
        5:'N',
        6:'I',
        7:'I, H',
        8:'N',
        9:'H, I'
    }

    for i in range(10):
        email = "sample" + str(i) + "@gmail.com"
        u, created = User.objects.get_or_create(username=email)
        u.set_unusable_password()
        u.userprofile.user_type = 'P'
        alphnum = string.ascii_uppercase + string.digits
        u.userprofile.user_url = ''.join(choice(alphnum) for x in range(6))
        u.userprofile.join_id = str(uuid.uuid1())
        provider_confirm_link = provider_confirm_url_prefix + u.userprofile.join_id
        u.userprofile.first_name = "First" + str(i)
        u.userprofile.last_name = "Last" + str(i)
        u.userprofile.phone = "123 - " + str(i)
        u.userprofile.zip_code = str(i) + str(i) + str(i) + str(i) + str(i)
        u.userprofile.country = "USA"
        u.userprofile.specialties_list = index_to_specialties_dict[i]
        u.userprofile.located_in = index_to_loc_dict[i]
        u.userprofile.payment_method = index_to_payment_dict[i]
        u.userprofile.pic_url = default_profile_pic_url
        u.userprofile.emailed = True
        u.save()
        u.userprofile.save()
    return None
    
