from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form= AuthenticationForm(request)
    context={'form':form}
    return render(request, 'accounts/login.html', context=context)

def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        username = request.POST.get('username')
        messages.success(request, f'Account was created for {username}.')
        return HttpResponseRedirect('/accounts/login/')
    context= {'form':form}
    return render(request, 'accounts/register.html', context=context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')