from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def home(request):
    return render(request, 'e_ikiraro/home.html', {'title': 'Home'})

def about(request):
    return render(request, 'e_ikiraro/about.html', {'title': 'About'})

def login(request):
    return render(request, 'e_ikiraro/login.html', {'title': 'Login'})

# def register(request):
#     return render(request, 'e_ikiraro/register.html', {'title': 'Register'})
