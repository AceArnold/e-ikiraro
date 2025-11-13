from django.urls import path, include
from ninja import NinjaAPI
from . import views
from applications import views as app_views

api = NinjaAPI()



urlpatterns = [
    path('', views.home, name='e-ikiraro-home'),
    path('about/', views.about, name='e-ikiraro-about'),
    # path('passport/', include('applications.urls')),
    path('documents/', views.documents, name='e-ikiraro-documents'),
    # path('login/', views.login, name='e-ikiraro-login'),
    # path('register/', views.register, name='e-ikiraro-register'),
] 