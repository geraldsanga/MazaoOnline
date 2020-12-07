from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from site_models.models import Order


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
            messages.success(request, "Welcome Back.")
            return redirect('home_page')
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html', {})


@login_required
def profile_view(request, id):
    user = User.objects.get(id=id)
    order_counter = int()
    onhold = int()
    for order in user.order_set.all():
        if order.ordered is True:
            order_counter += 1
        else:
            onhold += 1

    # Recent Orders
    queryset = Order.objects.filter(customer=user)[:3]

    # Updating profile details
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.profile.city = request.POST.get('city')
        user.profile.street_address = request.POST.get('street')
        user.profile.phone = request.POST.get('phone')
        user.save()

        messages.success(request, 'Profile Successfully updated.', fail_silently=False)

    return render(request, 'profile_view.html',{
        'object': User.objects.get(id=id),
        'order_counter': order_counter,
        'onhold': onhold,
        'qs': queryset
    })


def logout_view(request):
    logout(request)
    return redirect('login_view')
