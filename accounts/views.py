from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import update_session_auth_hash
from . models import *
from django.db.models import Sum

import random
import string
import math


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Username/Password is incorrect')
            return redirect('login')
    else:
        return render(request, "login.html")


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exist')
            else:
                user = User.objects.create_user(
                    username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                user.save()
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not match')
        return redirect('register')
    else:
        return render(request, "register.html")


def register_cinema(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        cinema_name = request.POST['cinema']
        phone = request.POST['phone']
        city = request.POST['city']
        address = request.POST['address']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exist')
            else:
                user = User.objects.create_user(
                    username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
                cin_user = Cinema(
                    cinema_name=cinema_name, phoneno=phone, city=city, address=address, user=user)
                cin_user.save()
                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not match')
        return redirect('register_cinema')
    else:
        return render(request, "register_cinema.html")


def register_studentclub(request):
    if request.method == 'POST':
        # student rep
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
       # password1 = request.POST['password1']
        dateofbirth = request.POST['dateofbirth']
        # student club
        club_name = request.POST['club']
        phone = request.POST['phone']
        city = request.POST['city']
        address = request.POST['address']
        postcode = request.POST['postcode']

        password1 = User.objects.make_random_password()

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username already exist')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email already exist')
        else:
            user = User.objects.create_user(

                username=username, first_name=first_name, last_name=last_name, email=email, password=password1)
            club_user = Club(
                club_name=club_name, club_phonenumber=phone, club_city=city, club_address=address, user=user, club_postcode=postcode, rep_dateofbirth=dateofbirth)
            club_user.save()
            messages.info(request, 'User created ' + "\n" +
                          "\n" + "Your unique password is: " + password1 + " make sure to keep this password safe")
            return redirect('login')

    else:
        return render(request, "register_studentclub.html")


def password(request):
    thepassword = "testing"
    return render(request, 'register_studentclub.html', {'password': thepassword})


def manager_register(request):
    if request.method == 'POST':
        username = request.POST['user']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already exist')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exist')
            else:
                user = User.objects.create_superuser(
                    username=username, first_name=first_name, last_name=last_name, email=email, password=password1, is_staff=True)

                cin_manager = CinemaManagerRegister(
                    user=user)
                cin_manager.save()

                messages.info(request, 'User created')
                return redirect('login')
        else:
            messages.info(request, 'Password not match')
        return redirect('manager_register')
    else:
        return render(request, "manager_register.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):
    u = request.user
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fn']
        last_name = request.POST['ln']
        email = request.POST['email']
        old = request.POST['password1']
        new = request.POST['new']
        user = User.objects.get(pk=u.pk)
        if User.objects.filter(username=username).exclude(pk=u.pk).exists():
            messages.error(request, 'Username already exists')

        elif User.objects.filter(email=email).exclude(pk=u.pk).exists():
            messages.error(request, 'Email already exists')

        elif user.check_password(old):
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.old = old
            user.set_password(new)
            user.save()
            # update session
            update_session_auth_hash(request, user)

            messages.success(request, 'Profile updated')
        else:
            messages.error(request, 'Wrong Old Password')

        return redirect('profile')

    else:
        user = request.user
        return render(request, "profile.html")


def bookings(request):
    user = request.user
    book = Bookings.objects.filter(user=user.pk)
    return render(request, "bookings.html", {'book': book})


def dashboard(request):
    user = request.user
    m = Shows.objects.filter(cinema=user.cinema).values(
        'movie', 'movie__movie_name', 'movie__movie_poster').distinct()
    print(m)
    return render(request, "dashboard.html", {'list': m})


def add_shows(request):
    user = request.user

    if request.method == 'POST':
        m = request.POST['m']
        t = request.POST['t']
        d = request.POST['d']
        p = request.POST['p']
        i = user.cinema.pk

        show = Shows(cinema_id=i, movie_id=m, date=d, time=t, price=p)
        show.save()
        messages.success(request, 'Show Added')
        return redirect('add_shows')

    else:
        m = Movie.objects.all()
        sh = Shows.objects.filter(cinema=user.cinema)
        data = {
            'mov': m,
            's': sh
        }
        return render(request, "add_shows.html", data)
