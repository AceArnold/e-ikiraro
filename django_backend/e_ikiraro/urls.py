from django.urls import path
from ninja import NinjaAPI
from . import views

api = NinjaAPI()



urlpatterns = [
    path('', views.home, name='e-ikiraro-home'),
    path('about/', views.about, name='e-ikiraro-about'),
    path('login/', views.login, name='e-ikiraro-login'),
    # path('register/', views.register, name='e-ikiraro-register'),
]