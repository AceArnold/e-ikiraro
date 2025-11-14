from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('start/', views.passport_application_start,
         name='passport-start'),
    path('apply/', views.passport_application_form,
         name='passport-apply'),
    path('payment/<uuid:application_id>/',
         views.passport_payment, name='passport-payment'),
    path('confirmation/<uuid:application_id>/',
         views.passport_confirmation, name='passport-confirmation'),
    path('my-applications/', views.my_applications, name='my-applications'),
    path('application/<uuid:application_id>/',
         views.application_detail, name='application-detail'),
    path('passport/test-start/', views.passport_application_start,
         name='passport-start-test'),
]
