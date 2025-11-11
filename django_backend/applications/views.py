from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import PassportApplicationForm
from e_ikiraro.models import PassportApplication, Application, Service, Payment
from decimal import Decimal
import uuid


@login_required
def passport_application_start(request):
    """Landing page for passport application"""
    try:
        passport_service = Service.objects.get(name='Passport Application')
    except Service.DoesNotExist:
        messages.error(request, 'Passport service is not available at the moment.')
        return redirect('e-ikiraro-home')
    
    context = {
        'title': 'Apply for Passport',
        'service': passport_service
    }
    return render(request, 'e_ikiraro/passport/passport_start.html', context)


@login_required
def passport_application_form(request):
    """Main passport application form"""
    if request.method == 'POST':
        form = PassportApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Get the passport service
                    passport_service = Service.objects.get(name='Passport Application')
                    
                    # Create the main application
                    application = Application.objects.create(
                        user=request.user,
                        service=passport_service,
                        status='Pending'
                    )
                    
                    # Create the passport application
                    passport_app = form.save(commit=False)
                    # If user is authenticated, fill missing personal fields from their profile
                    # (Django's auth.User has first_name, last_name, email)
                    if request.user.is_authenticated:
                        if not passport_app.first_name:
                            passport_app.first_name = request.user.first_name
                        if not passport_app.last_name:
                            passport_app.last_name = request.user.last_name
                        if not passport_app.email:
                            passport_app.email = request.user.email
                    passport_app.application = application
                    passport_app.save()
                    
                    # Store additional form data in session for payment
                    request.session['passport_app_data'] = {
                        'application_id': str(application.id),
                        'first_name': form.cleaned_data['first_name'],
                        'last_name': form.cleaned_data['last_name'],
                        'date_of_birth': form.cleaned_data['date_of_birth'].isoformat(),
                        'place_of_birth': form.cleaned_data['place_of_birth'],
                        'gender': form.cleaned_data['gender'],
                        'nationality': form.cleaned_data['nationality'],
                        'phone_number': form.cleaned_data['phone_number'],
                        'email': form.cleaned_data['email'],
                        'current_address': form.cleaned_data['current_address'],
                        'father_name': form.cleaned_data['father_name'],
                        'mother_name': form.cleaned_data['mother_name'],
                        'emergency_contact_name': form.cleaned_data['emergency_contact_name'],
                        'emergency_contact_phone': form.cleaned_data['emergency_contact_phone'],
                        'previous_passport_number': form.cleaned_data.get('previous_passport_number', ''),
                        'previous_passport_issue_date': form.cleaned_data.get('previous_passport_issue_date').isoformat() if form.cleaned_data.get('previous_passport_issue_date') else '',
                    }
                    
                    messages.success(request, 'Application submitted successfully! Please proceed to payment.')
                    return redirect('passport-payment', application_id=application.id)
                    
            except Service.DoesNotExist:
                messages.error(request, 'Passport service not found.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        # Prefill form with logged-in user's basic info so they don't need to retype it
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            form = PassportApplicationForm(initial=initial)
        else:
            form = PassportApplicationForm()
    
    context = {
        'title': 'Passport Application Form',
        'form': form
    }
    return render(request, 'applications/passport_form.html', context)


@login_required
def passport_payment(request, application_id):
    """Payment page for passport application"""
    application = get_object_or_404(Application, id=application_id, user=request.user)
    
    # Check if payment already exists
    existing_payment = Payment.objects.filter(
        application=application,
        status='Completed'
    ).first()
    
    if existing_payment:
        messages.info(request, 'Payment already completed for this application.')
        return redirect('passport-confirmation', application_id=application.id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        phone_number = request.POST.get('phone_number')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('passport-payment', application_id=application.id)
        
        try:
            with transaction.atomic():
                # Create payment record
                payment = Payment.objects.create(
                    user=request.user,
                    application=application,
                    service_type='Passport Application',
                    amount=application.service.base_fee,
                    payment_method=payment_method,
                    transaction_id=f'TXN-{uuid.uuid4().hex[:12].upper()}',
                    provider_reference=f'REF-{uuid.uuid4().hex[:12].upper()}',
                    status='Completed'  # In production, this would be 'Pending' until confirmed
                )
                
                # Update application status
                application.status = 'Submitted'
                application.save()
                
                messages.success(request, 'Payment successful! Your application has been submitted.')
                return redirect('passport-confirmation', application_id=application.id)
                
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')
    
    context = {
        'title': 'Payment',
        'application': application,
        'service': application.service,
        'amount': application.service.base_fee
    }
    return render(request, 'e_ikiraro/passport/passport_payment.html', context)


@login_required
def passport_confirmation(request, application_id):
    """Confirmation page after successful application"""
    application = get_object_or_404(Application, id=application_id, user=request.user)
    passport_app = get_object_or_404(PassportApplication, application=application)
    payment = Payment.objects.filter(application=application).first()
    
    # Get stored application data from session
    app_data = request.session.get('passport_app_data', {})
    
    context = {
        'title': 'Application Confirmation',
        'application': application,
        'passport_app': passport_app,
        'payment': payment,
        'app_data': app_data
    }
    return render(request, 'e_ikiraro/passport/passport_confirmation.html', context)


@login_required
def my_applications(request):
    """View all user's passport applications"""
    applications = Application.objects.filter(
        user=request.user,
        service__name='Passport Application'
    ).order_by('-submitted_at')
    
    context = {
        'title': 'My Applications',
        'applications': applications
    }
    return render(request, 'e_ikiraro/passport/my_applications.html', context)


@login_required
def application_detail(request, application_id):
    """View details of a specific application"""
    application = get_object_or_404(Application, id=application_id, user=request.user)
    passport_app = get_object_or_404(PassportApplication, application=application)
    payments = Payment.objects.filter(application=application)
    
    context = {
        'title': 'Application Details',
        'application': application,
        'passport_app': passport_app,
        'payments': payments
    }
    return render(request, 'e_ikiraro/passport/application_detail.html', context)