from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


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

