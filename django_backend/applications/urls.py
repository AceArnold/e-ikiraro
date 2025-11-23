from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('start/', views.passport_application_start,
         name='passport-start'),
    path('apply/', views.passport_application_form,
         name='passport-apply'),
    # National ID
    path('national-id/start/', views.nationalid_application_start,
         name='nationalid-start'),
    path('national-id/apply/', views.nationalid_application_form,
         name='nationalid-apply'),
    path('national-id/payment/<uuid:application_id>/',
         views.nationalid_payment, name='nationalid-payment'),
    path('national-id/confirmation/<uuid:application_id>/',
         views.nationalid_confirmation, name='nationalid-confirmation'),
    # Driver's License
    path('license/start/', views.drivers_license_application_start,
         name='license-start'),
    path('license/apply/', views.drivers_license_application_form,
         name='license-apply'),
    path('license/payment/<uuid:application_id>/',
         views.drivers_license_payment, name='license-payment'),
    path('license/confirmation/<uuid:application_id>/',
         views.drivers_license_confirmation, name='license-confirmation'),
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
