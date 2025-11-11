from django.urls import path
from . import views as app_views

app_name = 'applications'

urlpatterns = [
    path('start/', app_views.passport_application_start, name='passport-start'),
    path('apply/', app_views.passport_application_form, name='passport-apply'),
    path('payment/<uuid:application_id>/', app_views.passport_payment, name='passport-payment'),
    path('confirmation/<uuid:application_id>/', app_views.passport_confirmation, name='passport-confirmation'),
    path('my-applications/', app_views.my_applications, name='my-applications'),
    path('application/<uuid:application_id>/', app_views.application_detail, name='application-detail'),
    path('passport/test-start/', app_views.passport_application_start, name='passport-start-test'),
]