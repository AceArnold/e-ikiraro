from django.urls import path
from . import passport_views

urlpatterns = [
    path('start/', passport_views.passport_application_start, name='passport-start'),
    path('apply/', passport_views.passport_application_form, name='passport-apply'),
    path('payment/<uuid:application_id>/', passport_views.passport_payment, name='passport-payment'),
    path('confirmation/<uuid:application_id>/', passport_views.passport_confirmation, name='passport-confirmation'),
    path('my-applications/', passport_views.my_applications, name='my-applications'),
    path('application/<uuid:application_id>/', passport_views.application_detail, name='application-detail'),