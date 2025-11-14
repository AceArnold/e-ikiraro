from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import PassportApplicationForm
from e_ikiraro.models import PassportApplication, Service, Payment, Document
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
    return render(request, 'applications/passport_start.html', context)


@login_required
def passport_application_form(request):
    """Main passport application form"""
    if request.method == 'POST':
        form = PassportApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the passport application directly
                    passport_app = form.save(commit=False)
                    passport_app.user = request.user
                    # If user is authenticated, fill missing personal fields from their profile
                    # (Django's auth.User has first_name, last_name, email)
                    if request.user.is_authenticated:
                        if not passport_app.first_name:
                            passport_app.first_name = request.user.first_name
                        if not passport_app.last_name:
                            passport_app.last_name = request.user.last_name
                        if not passport_app.email:
                            passport_app.email = request.user.email
                    passport_app.save()

                    # Create Document records so uploaded files appear in the Documents table
                    try:
                        if passport_app.passport_photo:
                            Document.objects.create(
                                user=request.user,
                                passport_application=passport_app,
                                document_type='Passport Photo',
                                file=passport_app.passport_photo
                            )
                        if passport_app.birth_certificate:
                            Document.objects.create(
                                user=request.user,
                                passport_application=passport_app,
                                document_type='Birth Certificate',
                                file=passport_app.birth_certificate
                            )
                        if passport_app.national_id:
                            Document.objects.create(
                                user=request.user,
                                passport_application=passport_app,
                                document_type='National ID',
                                file=passport_app.national_id
                            )
                    except Exception:
                        # Don't fail the whole submission if Document creation fails; app already saved.
                        pass

                    # Store additional form data in session for payment
                    request.session['passport_app_data'] = {
                        'application_id': str(passport_app.id),
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
                    return redirect('applications:passport-payment', application_id=passport_app.id)

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
    passport_app = get_object_or_404(PassportApplication, id=application_id, user=request.user)

    # Check if payment already exists
    existing_payment = Payment.objects.filter(
        passport_application=passport_app,
        status='Completed'
    ).first()

    if existing_payment:
        messages.info(request, 'Payment already completed for this application.')
        return redirect('applications:passport-confirmation', application_id=passport_app.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        phone_number = request.POST.get('phone_number')

        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('passport-payment', application_id=passport_app.id)

        try:
            with transaction.atomic():
                # Get the service fee
                passport_service = Service.objects.get(name='Passport Application')
                # Create payment record
                payment = Payment.objects.create(
                    user=request.user,
                    passport_application=passport_app,
                    service_type='Passport Application',
                    amount=passport_service.base_fee,
                    payment_method=payment_method,
                    transaction_id=f'TXN-{uuid.uuid4().hex[:12].upper()}',
                    provider_reference=f'REF-{uuid.uuid4().hex[:12].upper()}',
                    status='Completed'  # In production, this would be 'Pending' until confirmed
                )

                # Update application status
                passport_app.status = 'Submitted'
                passport_app.save()

                # Send confirmation email with receipt
                try:
                    subject = f'Application Confirmation - {passport_service.name}'
                    html_message = render_to_string('applications/application_confirmation_email.html', {
                        'first_name': passport_app.first_name,
                        'last_name': passport_app.last_name,
                        'service_type': passport_service.name,
                        'application_id': str(passport_app.id),
                        'submitted_at': passport_app.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': passport_app.status,
                        'transaction_id': payment.transaction_id,
                        'amount': payment.amount,
                        'payment_method': payment.payment_method,
                        'paid_at': payment.paid_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'provider_reference': payment.provider_reference,
                    })
                    plain_message = strip_tags(html_message)
                    from_email = settings.EMAIL_FROM
                    to_email = passport_app.email

                    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
                except Exception as e:
                    # Log the error but don't fail the application process
                    print(f"Failed to send confirmation email: {str(e)}")

                messages.success(request, 'Payment successful! Your application has been submitted.')
                return redirect('applications:passport-confirmation', application_id=passport_app.id)

        except Service.DoesNotExist:
            messages.error(request, 'Passport service not found.')
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')

    # Get service for context
    passport_service = Service.objects.get(name='Passport Application')

    context = {
        'title': 'Payment',
        'passport_app': passport_app,
        'service': passport_service,
        'amount': passport_service.base_fee
    }
    return render(request, 'applications/passport_payment.html', context)


@login_required
def passport_confirmation(request, application_id):
    """Confirmation page after successful application"""
    passport_app = get_object_or_404(PassportApplication, id=application_id, user=request.user)
    payment = Payment.objects.filter(passport_application=passport_app).first()

    # Get stored application data from session
    app_data = request.session.get('passport_app_data', {})

    context = {
        'title': 'Application Confirmation',
        'passport_app': passport_app,
        'payment': payment,
        'app_data': app_data
    }
    return render(request, 'applications/passport_confirmation.html', context)


@login_required
def my_applications(request):
    """View all user's passport applications"""
    applications = PassportApplication.objects.filter(
        user=request.user
    ).order_by('-submitted_at')

    context = {
        'title': 'My Applications',
        'applications': applications
    }
    return render(request, 'applications/my_applications.html', context)


@login_required
def application_detail(request, application_id):
    """View details of a specific application"""
    passport_app = get_object_or_404(PassportApplication, id=application_id, user=request.user)
    payments = Payment.objects.filter(passport_application=passport_app)

    context = {
        'title': 'Application Details',
        'passport_app': passport_app,
        'payments': payments
    }
    return render(request, 'applications/application_detail.html', context)
