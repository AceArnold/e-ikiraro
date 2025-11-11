from django.urls import path, include
from ninja import NinjaAPI
from . import views

api = NinjaAPI()

urlpatterns = [
    path('', views.home, name='e-ikiraro-home'),
    path('about/', views.about, name='e-ikiraro-about'),
    path('passport/', include('e_ikiraro.passport_urls')),  # Add this line
]