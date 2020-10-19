from django.core.mail import send_mail
from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.generic import TemplateView

from sub.forms import AdoptForm
from sub.models import *


# Create your views here.
def home(request):
    return render(request, 'prac.html')


def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        elif username == '' or password == '':
            message = "Missing password/username details !!!"
            context = {
                'message': message,
            }
            return render(request, 'login.html', context)
        else:
            message = "Wrong details entered!!!"
            context = {
                'message': message,
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        firstn = request.POST['firstname']
        lastn = request.POST['lastname']
        zip = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=zip).exists():
            message = "Username Already exists!!!"
            context = {
                'message': message,
            }
            return render(request, 'register.html', context)
        if User.objects.filter(email=email).exists():
            message = "Email Already exists!!!"
            context = {
                'message': message,
            }
            return render(request, 'register.html', context)
        if zip != '' and password != '' and email != '':
            if '.com' in email and '@' in email:
                user = User.objects.create_user(username=zip, password=password, email=email, first_name=firstn,
                                                last_name=lastn)
                user.save()
                send_mail('Registration Successful.',
                          'Dear User,\n\t You are now part of the NGO Family. We would try our best to please you providing the best services and offers we can.',
                          'settings.EMAIL_HOST_USER',
                          [email],
                          fail_silently=False, )
            else:
                message = "Invalid Email entered!!!"
                context = {
                    'message': message,
                }
                return render(request, 'register.html', context)
        else:

            message = "Missing email/password/username details !!!"
            context = {
                'message': message,
            }
            return render(request, 'register.html', context)
        return redirect('login')
    else:
        return render(request, 'register.html')


def volun(request):
    return render(request, 'volun.html')


def donate(request):
    return render(request, 'donate.html')

def pay(request):
    return render(request, 'pay.html')

def adform(request):
    if request.user.is_authenticated:
        if Adopt.objects.filter(name=request.user.first_name).exists():
            message = "Your Adoption Form is already submitted and pending"
            context = {
                'message': message,
            }
            return render(request, 'prac.html', context)
        return render(request, 'adform.html')
    else:
        message = "You need to login first!!!"
        context = {
            'message': message,
        }
        return render(request, 'login.html', context)


def adopt(request):
    if request.method == "POST":
        MyAdoptForm = AdoptForm(request.POST, request.FILES)
        # Get the posted form
        MyAdoptForm.is_valid()
        adopt = Adopt()
        adopt.name = request.user.first_name

        # adopt.phone = MyAdoptForm.cleaned_data['phone']
        adopt.phone = request.POST.get('phone')
        adopt.mes = request.POST.get('mes')
        adopt.doc = request.POST.get('doc')
        adopt.email = request.user.email
        adopt.pictures = request.FILES.get('pictures')
        if adopt.phone == '' or adopt.doc == 'CHOOSE DOCUMENT...' or adopt.pictures == None:
            message = "Please fill all the details in the form"
            context = {
                'message': message,
            }
            return render(request, 'adform.html', context)
        else:
            adopt.save()
            send_mail('NGOrphan has recieved you Adoption Form.',
                      'Dear user,\n\t You have successfully taken your first step towards adopting a child. You will recieve a call from our representitive within next 72 hours.',
                      'settings.EMAIL_HOST_USER',
                      [adopt.email],
                      fail_silently=False, )
            return redirect('profile')
    else:
        MyAdoptForm = AdoptForm()
    return redirect('home')


def action(request):
    return render(request, 'action.html')


def laws(request):
    return render(request, 'laws.html')


def campaign(request):
    data = camp.objects.all()
    context = {'data': data}
    name = request.POST.get('user_name')
    if name != "":
        if request.method == "POST":
            title = request.POST.get('title')
            venue = request.POST.get('venue')
            time = request.POST.get('time')
            date = request.POST.get('date')
            month = request.POST.get('month')
            if profile.objects.filter(title=title, usname=name).exists():
                message = "This event is already added!!!"
                context = {
                    'message': message,
                }
                return render(request, 'prac.html', context)
            else:
                list = profile(usname=name, title=title, venue=venue, time=time, date=date, month=month)
                list.save()
        return render(request, 'camp.html', context)
    else:
        message = "You need to login first!!!"
        context = {
            'message': message,
        }
        return render(request, 'login.html', context)


def profiles(request):
    all_event = profile.objects.filter(usname=request.user.first_name)
    data=Adopt.objects.filter(email=request.user.email)
    context={
        'events':all_event,
        'data':data,
    }

    return render(request, 'mama.html', context)

def rem(request, title):
    profile.objects.filter(title=title, usname=request.user.first_name).delete()
    return profiles(request)


def logout(request):
    auth.logout(request)
    return redirect('login')
