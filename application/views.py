from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def index(request):
    return render(request, 'application/index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, 'There was an error logging in, try again ...')
            return redirect('login')
    else:
        return render(request, 'authentication/login.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        return redirect('index')
    else:
        return render(request, 'authentication/register.html')


@login_required(login_url='login')
def profile(request):
    return render(request, 'application/profile.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
