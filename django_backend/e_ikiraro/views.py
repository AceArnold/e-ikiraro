from django.shortcuts import render
from django.http import HttpResponse 
from .models import Document

# Create your views here.

def home(request):
    return render(request, 'e_ikiraro/home.html', {'title': 'Home'})

def about(request):
    return render(request, 'e_ikiraro/about.html', {'title': 'About'})

def documents(request):
    """View to display uploaded documents"""
    # If user is authenticated, show their documents. Otherwise show all.
    if request.user.is_authenticated:
        docs = Document.objects.filter(user=request.user)
    else:
        docs = Document.objects.all()
    
    return render(request, 'e_ikiraro/documents.html', {
        'title': 'Documents',
        'documents': docs
    })

# def login(request):
#     return render(request, 'e_ikiraro/login.html', {'title': 'Login'})

# def register(request):
#     return render(request, 'e_ikiraro/register.html', {'title': 'Register'})
