from django.shortcuts import render,redirect, get_object_or_404
from LetsMakeAGroup.forms import *
from django.core.urlresolvers import reverse
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.db import transaction
from django.http import Http404
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail
# Used to send a real email
import smtplib
from email.mime.text import MIMEText

def signin(request):
  return render(request, 'signin.html', {})

@transaction.commit_on_success
def signup(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'signup.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'signup.html', context)
    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['username'])
    new_user.is_active = False
    new_user.save()

    if 'picture' in request.FILES and request.FILES['picture']:
        picture = request.FILES['picture']
    else:
        picture = 'info-photos/anonymous.png'
    new_info = Info(user=new_user,firstname = form.cleaned_data['firstname'], lastname = form.cleaned_data['lastname'],   \
                    email=form.cleaned_data['username'], picture=picture)
    new_info.save()
    newuserfollowers = UserFollowers(user = new_user)
    newuserfollowers.save()
 #   new_user = authenticate(username=form.cleaned_data['username'], \
 #                           password=form.cleaned_data['password1'])
 #   login(request, new_user)
 #   return redirect('/')
    token = default_token_generator.make_token(new_user)

    fromaddr = 'LetsMakeAGroup@gmail.com'
    toaddrs  = new_user.email
    # Credentials information
    username = 'LetsMakeAGroup@gmail.com'
    password = 'LetsMakeAGroupCMU'

    email_body = """
Welcome to LetsMakeAGroup! Please click the link below to
verify your email address and complete the registration of your account:

  http://%s%s
""" % (request.get_host(),
       reverse('confirm', args=(new_user.username, token)))

    message = MIMEText(email_body)
    message['Subject'] = 'Registration confirm from LetsMakeAGroup'
    message['From'] = fromaddr
    message['To'] = toaddrs

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, message.as_string())
    server.quit()

    '''
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="fangxiaf@andrew.cmu.edu",
              recipient_list=[new_user.email])
    '''
    context['email'] = form.cleaned_data['username']
    return render(request, 'needs-confirmation.html', context)



@transaction.commit_on_success
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})

def getbackpassword(request, username, token):
    context = {}
    user = get_object_or_404(User, username=username)
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    # Otherwise token was valid, activate the user.
    context['username']=username
    context['token']=token
    return render(request, 'getbackpassword.html', context)

@transaction.commit_on_success
def resetpassword(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'signin.html', context)
    if not 'new' in request.POST or not request.POST['new'] or not 'confirm' in request.POST or not request.POST['confirm'] :
        context = {"errors": "New Password and Confirm Password are both required.","username":requst.POST['username']}
        return render(request, 'forgetpassword.html', context)
    if request.POST['new']!=request.POST['confirm']:
        context = {"errors": "Passwords do not match.","username":request.POST['username']}
        return render(request, 'forgetpassword.html', context)

    user = get_object_or_404(User, username=request.POST['username'])
    password = request.POST['new']
    user.set_password(password)
    user.save()
    # Send 404 error if token is invalid

    return render(request, 'afterreset.html')


@transaction.commit_on_success
def forget_password(request):
    context = {}
    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return redirect('/signin.html')
    if not 'email' in request.POST or not request.POST['email']:
        context = {"errors":"You need to enter your email to reset password."}
        return render(request, 'signin.html', context)

    user = User.objects.filter(username = request.POST['email'])

    if not user:
        error = "Invalid Email."
        context = {"errors":error}
        return render(request, 'signin.html', context)
    user = User.objects.get(username = request.POST['email'])
    token = default_token_generator.make_token(user)

    # Contact information
    fromaddr = 'LetsMakeAGroup@gmail.com'
    toaddrs  = user.email
    # Credentials information
    username = 'LetsMakeAGroup@gmail.com'
    password = 'LetsMakeAGroupCMU'

    email_body = """
Click the link below to reset your password:

  http://%s%s
""" % (request.get_host(),
       reverse('getbackpassword', args=(user.username, token)))

    message = MIMEText(email_body)
    message['Subject'] = 'Change Password From LetsMakeAGroup'
    message['From'] = fromaddr
    message['To'] = toaddrs

    #Connect to server and send the email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, message.as_string())
    server.quit()

    '''
    send_mail(subject="Grumbls password",
              message= email_body,
              from_email="fangxiaf@andrew.cmu.edu",
              recipient_list=[user.email])
    '''
    return render(request, 'aftersend.html')



@transaction.commit_on_success
def resetpassword_signin(request):
    context = {}
    if request.method == 'GET':
        return redirect('/signin.html')
    if not 'email' in request.POST or not request.POST['email'] or not 'current' in request.POST or not request.POST['current']  \
        or not 'new' in request.POST or not request.POST['new'] or not 'confirm' in request.POST or not request.POST['confirm']:
        context = {"errors":"Incompleted Input"}
        return render(request, 'signin.html', context)

    user = User.objects.filter(username = request.POST['email'])
    if not user:
        error = "Invalid Email."
        context = {"errors":error}
        return render(request, 'signin.html', context)
    user = User.objects.get(username = request.POST['email'])
    oldpassword = request.POST['current']
    if not user.check_password(oldpassword):
        error = "Current password is not correct."
        context = {"errors":error}
        return render(request, 'signin.html', context)
    if request.POST['new'] != request.POST['confirm']:
        error = "Your passwords do not match."
        context = {"errors":error}
        return render(request, 'signin.html', context)
    user.set_password(request.POST['new'])
    user.save()
    return render(request, 'afterreset.html')
