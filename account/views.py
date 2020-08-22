from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        try:
            User.objects.get(username=username)
            print("username taken")
            messages.error(request, "This username is already taken")
        except:
            if password == password2:
                User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
                user_to_login = authenticate(username=username, password=password)
                login(request, user_to_login)
                return redirect('home_page')
            else:
                print("passwords did not match")
                messages.error(request, "Your passwords did not match")
    return render(request, 'register.html', {})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('login_view')
