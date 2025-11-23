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
from .forms import PassportApplicationForm, DriversLicenseApplicationForm, NationalIDApplicationForm
from e_ikiraro.models import PassportApplication, Service, Payment, Document, DriversLicenseApplication, NationalIDApplication
from decimal import Decimal
import uuid


@login_required
def passport_application_start(request):
    """Landing page for passport application"""
    # Try a flexible lookup so the exact name in the DB doesn't break the flow
    passport_service = Service.objects.filter(
        name__icontains='passport').first()
    if not passport_service:
        messages.error(
            request, 'Passport service is not available at the moment.')
        return redirect('e-ikiraro-home')

    # Render the generic service start template for passport with specific context
    required_documents = [
        'Recent passport-sized photograph (JPEG/PNG)',
        'Birth certificate (PDF/Image)',
        'National ID card (PDF/Image)',
        'Previous passport (if renewal)'
    ]
    process_steps = [
        'Fill out the application form with accurate information',
        'Upload required documents',
        'Make payment using Mobile Money, Bank Transfer, or Credit Card',
        'Receive confirmation and track your application',
        'Collect your passport when ready'
    ]
    return render(request, 'applications/service_start.html', {
        'title': 'Apply for Passport',
        'service': passport_service,
        'required_documents': required_documents,
        'process_steps': process_steps,
        'processing_time': 'Typically 10-15 business days',
        'apply_url_name': 'applications:passport-apply',
        'extra_info_title': 'Passport Types:',
        'extra_info_list': ['Ordinary Passport', 'Official Passport', 'Diplomatic Passport', 'Emergency Travel Document'],
        'lead_text': 'Apply for your Burundian passport online quickly and securely.'
    })


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

                    messages.success(
                        request, 'Application submitted successfully! Please proceed to payment.')
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
    passport_app = get_object_or_404(
        PassportApplication, id=application_id, user=request.user)

    # Check if payment already exists
    existing_payment = Payment.objects.filter(
        passport_application=passport_app,
        status='Completed'
    ).first()

    if existing_payment:
        messages.info(
            request, 'Payment already completed for this application.')
        return redirect('applications:passport-confirmation', application_id=passport_app.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        phone_number = request.POST.get('phone_number')

        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('passport-payment', application_id=passport_app.id)

        try:
            with transaction.atomic():
                # Get the service fee (flexible lookup)
                passport_service = Service.objects.filter(
                    name__icontains='passport').first()
                if not passport_service:
                    raise Service.DoesNotExist('Passport service not found')
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

                    send_mail(subject, plain_message, from_email, [
                              to_email], html_message=html_message)
                except Exception as e:
                    # Log the error but don't fail the application process
                    print(f"Failed to send confirmation email: {str(e)}")

                messages.success(
                    request, 'Payment successful! Your application has been submitted.')
                return redirect('applications:passport-confirmation', application_id=passport_app.id)

        except Service.DoesNotExist:
            messages.error(request, 'Passport service not found.')
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')

    # Get service for context (flexible lookup)
    passport_service = Service.objects.filter(
        name__icontains='passport').first()
    if not passport_service:
        passport_service = None

    context = {
        'title': 'Payment',
        'passport_app': passport_app,
        'application': passport_app,
        'service': passport_service,
        'amount': passport_service.base_fee if passport_service else Decimal('0.00')
    }
    return render(request, 'applications/passport_payment.html', context)


@login_required
def passport_confirmation(request, application_id):
    """Confirmation page after successful application"""
    passport_app = get_object_or_404(
        PassportApplication, id=application_id, user=request.user)
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
    # Combine different application types for the user
    passport_apps = PassportApplication.objects.filter(
        user=request.user).order_by('-submitted_at')
    national_id_apps = NationalIDApplication.objects.filter(
        user=request.user).order_by('-submitted_at')
    drivers_license_apps = DriversLicenseApplication.objects.filter(
        user=request.user).order_by('-submitted_at')

    # For simplicity, the template can handle separate lists or you could normalize into a single list
    context = {
        'title': 'My Applications',
        'passport_applications': passport_apps,
        'national_id_applications': national_id_apps,
        'drivers_license_applications': drivers_license_apps,
    }
    return render(request, 'applications/my_applications.html', context)


@login_required
def application_detail(request, application_id):
    """View details of a specific application"""
    # Try to find the application in each application model so a single
    # detail view can show passport, national id or driver's license apps.
    passport_app = PassportApplication.objects.filter(
        id=application_id, user=request.user).first()
    if passport_app:
        payments = Payment.objects.filter(passport_application=passport_app)
        context = {'title': 'Application Details',
                   'passport_app': passport_app, 'payments': payments}
        return render(request, 'applications/application_detail.html', context)

    nid_app = NationalIDApplication.objects.filter(
        id=application_id, user=request.user).first()
    if nid_app:
        payments = Payment.objects.filter(national_id_application=nid_app)
        # reuse the passport template by passing nid_app as `passport_app`
        context = {'title': 'Application Details',
                   'passport_app': nid_app, 'payments': payments}
        return render(request, 'applications/application_detail.html', context)

    dl_app = DriversLicenseApplication.objects.filter(
        id=application_id, user=request.user).first()
    if dl_app:
        payments = Payment.objects.filter(drivers_license_application=dl_app)
        context = {'title': 'Application Details',
                   'passport_app': dl_app, 'payments': payments}
        return render(request, 'applications/application_detail.html', context)

    # If not found in any, return 404
    return HttpResponse(status=404)


# --------------------- National ID flow ---------------------
@login_required
def nationalid_application_start(request):
    # Flexible lookup for National ID service
    nid_service = Service.objects.filter(name__icontains='national').first()
    if not nid_service:
        messages.error(
            request, 'National ID service is not available at the moment.')
        return redirect('e-ikiraro-home')

    # Render the generic service start template with National ID specifics
    required_documents = [
        'Birth certificate (PDF/Image)'
    ]
    process_steps = [
        'Fill out the application form with accurate information',
        'Upload required documents',
        'Make payment using Mobile Money, Bank Transfer, or Credit Card',
        'Receive confirmation and track your application'
    ]
    return render(request, 'applications/service_start.html', {
        'title': 'Apply for National ID',
        'service': nid_service,
        'required_documents': required_documents,
        'process_steps': process_steps,
        'processing_time': 'Varies depending on workload',
        'apply_url_name': 'applications:nationalid-apply',
        'lead_text': 'Apply for your National ID online quickly and securely.'
    })


@login_required
def nationalid_application_form(request):
    if request.method == 'POST':
        form = NationalIDApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    nid_app = form.save(commit=False)
                    nid_app.user = request.user
                    nid_app.save()

                    # Save document record
                    try:
                        if nid_app.birth_certificate:
                            Document.objects.create(
                                user=request.user,
                                national_id_application=nid_app,
                                document_type='Birth Certificate',
                                file=nid_app.birth_certificate
                            )
                    except Exception:
                        pass

                    request.session['nationalid_app_data'] = {
                        'application_id': str(nid_app.id),
                    }
                    messages.success(
                        request, 'Application submitted. Proceed to payment.')
                    return redirect('applications:nationalid-payment', application_id=nid_app.id)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = NationalIDApplicationForm()

    return render(request, 'applications/nationalid_form.html', {'title': 'National ID Application Form', 'form': form})


@login_required
def nationalid_payment(request, application_id):
    nid_app = get_object_or_404(
        NationalIDApplication, id=application_id, user=request.user)

    existing_payment = Payment.objects.filter(
        national_id_application=nid_app, status='Completed').first()
    if existing_payment:
        messages.info(
            request, 'Payment already completed for this application.')
        return redirect('applications:nationalid-confirmation', application_id=nid_app.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('applications:nationalid-payment', application_id=nid_app.id)

        try:
            with transaction.atomic():
                nid_service = Service.objects.filter(
                    name__icontains='national').first()
                if not nid_service:
                    raise Service.DoesNotExist('National ID service not found')

                payment = Payment.objects.create(
                    user=request.user,
                    national_id_application=nid_app,
                    service_type='National ID Application',
                    amount=nid_service.base_fee,
                    payment_method=payment_method,
                    transaction_id=f'TXN-{uuid.uuid4().hex[:12].upper()}',
                    provider_reference=f'REF-{uuid.uuid4().hex[:12].upper()}',
                    status='Completed'
                )

                nid_app.status = 'Submitted'
                nid_app.save()

                # send email (reuse logic)
                try:
                    subject = f'Application Confirmation - {nid_service.name}'
                    html_message = render_to_string('applications/application_confirmation_email.html', {
                        'first_name': getattr(nid_app, 'first_name', ''),
                        'last_name': getattr(nid_app, 'last_name', ''),
                        'service_type': nid_service.name,
                        'application_id': str(nid_app.id),
                        'submitted_at': nid_app.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': nid_app.status,
                        'transaction_id': payment.transaction_id,
                        'amount': payment.amount,
                        'payment_method': payment.payment_method,
                        'paid_at': payment.paid_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'provider_reference': payment.provider_reference,
                    })
                    plain_message = strip_tags(html_message)
                    from_email = settings.EMAIL_FROM
                    to_email = getattr(nid_app, 'email', request.user.email)
                    send_mail(subject, plain_message, from_email, [
                              to_email], html_message=html_message)
                except Exception as e:
                    print(f'Failed to send confirmation email: {e}')

                messages.success(
                    request, 'Payment successful! Your application has been submitted.')
                return redirect('applications:nationalid-confirmation', application_id=nid_app.id)
        except Service.DoesNotExist:
            messages.error(request, 'Service not found.')
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')

    nid_service = Service.objects.filter(name__icontains='national').first()
    if not nid_service:
        nid_service = None
    context = {'title': 'Payment', 'application': nid_app,
               'service': nid_service, 'amount': nid_service.base_fee if nid_service else Decimal('0.00')}
    return render(request, 'applications/passport_payment.html', context)


@login_required
def nationalid_confirmation(request, application_id):
    nid_app = get_object_or_404(
        NationalIDApplication, id=application_id, user=request.user)
    payment = Payment.objects.filter(national_id_application=nid_app).first()
    app_data = request.session.get('nationalid_app_data', {})
    return render(request, 'applications/passport_confirmation.html', {'title': 'Confirmation', 'passport_app': nid_app, 'payment': payment, 'app_data': app_data})


# --------------------- Driver's License flow ---------------------
@login_required
def drivers_license_application_start(request):
    # Flexible lookup for Driver's License service
    svc = Service.objects.filter(name__icontains='driver').first()
    if not svc:
        messages.error(
            request, "Driver's License service is not available at the moment.")
        return redirect('e-ikiraro-home')
    # Render the generic service start template with Driver's License specifics
    required_documents = [
        'Recent photo (JPEG/PNG)',
        'National ID (PDF/Image)',
        'Medical certificate (PDF/Image)',
        'Eye test certificate (PDF/Image)'
    ]
    process_steps = [
        'Fill out the application form with accurate information',
        'Upload required documents',
        'Make payment using Mobile Money, Bank Transfer, or Credit Card',
        'Receive confirmation and track your application'
    ]
    return render(request, 'applications/service_start.html', {
        'title': 'Apply for Driver License',
        'service': svc,
        'required_documents': required_documents,
        'process_steps': process_steps,
        'processing_time': 'Varies depending on workload',
        'apply_url_name': 'applications:license-apply',
        'lead_text': "Apply for your Driver's License online and upload the required certificates."
    })


@login_required
def drivers_license_application_form(request):
    if request.method == 'POST':
        form = DriversLicenseApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    dl_app = form.save(commit=False)
                    dl_app.user = request.user
                    dl_app.save()

                    # create Document records
                    try:
                        if dl_app.photo:
                            Document.objects.create(
                                user=request.user, drivers_license_application=dl_app, document_type='Driver Photo', file=dl_app.photo)
                        if dl_app.medical_certificate:
                            Document.objects.create(user=request.user, drivers_license_application=dl_app,
                                                    document_type='Medical Certificate', file=dl_app.medical_certificate)
                        if dl_app.eye_test_certificate:
                            Document.objects.create(user=request.user, drivers_license_application=dl_app,
                                                    document_type='Eye Test Certificate', file=dl_app.eye_test_certificate)
                    except Exception:
                        pass

                    request.session['drivers_license_app_data'] = {
                        'application_id': str(dl_app.id)}
                    messages.success(
                        request, 'Application submitted. Proceed to payment.')
                    return redirect('applications:license-payment', application_id=dl_app.id)
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
    else:
        form = DriversLicenseApplicationForm()

    return render(request, 'applications/drivers_license_form.html', {'title': 'Driver License Application Form', 'form': form})


@login_required
def drivers_license_payment(request, application_id):
    dl_app = get_object_or_404(
        DriversLicenseApplication, id=application_id, user=request.user)
    existing_payment = Payment.objects.filter(
        drivers_license_application=dl_app, status='Completed').first()
    if existing_payment:
        messages.info(
            request, 'Payment already completed for this application.')
        return redirect('applications:license-confirmation', application_id=dl_app.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('applications:license-payment', application_id=dl_app.id)
        try:
            with transaction.atomic():
                svc = Service.objects.filter(name__icontains='driver').first()
                if not svc:
                    raise Service.DoesNotExist(
                        "Driver's License service not found")
                payment = Payment.objects.create(
                    user=request.user,
                    drivers_license_application=dl_app,
                    service_type="Driver's License Application",
                    amount=svc.base_fee,
                    payment_method=payment_method,
                    transaction_id=f'TXN-{uuid.uuid4().hex[:12].upper()}',
                    provider_reference=f'REF-{uuid.uuid4().hex[:12].upper()}',
                    status='Completed'
                )
                dl_app.status = 'Submitted'
                dl_app.save()
                # send email
                try:
                    subject = f'Application Confirmation - {svc.name}'
                    html_message = render_to_string('applications/application_confirmation_email.html', {
                        'first_name': getattr(dl_app, 'first_name', ''),
                        'last_name': getattr(dl_app, 'last_name', ''),
                        'service_type': svc.name,
                        'application_id': str(dl_app.id),
                        'submitted_at': dl_app.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': dl_app.status,
                        'transaction_id': payment.transaction_id,
                        'amount': payment.amount,
                        'payment_method': payment.payment_method,
                        'paid_at': payment.paid_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'provider_reference': payment.provider_reference,
                    })
                    plain_message = strip_tags(html_message)
                    from_email = settings.EMAIL_FROM
                    to_email = getattr(dl_app, 'email', request.user.email)
                    send_mail(subject, plain_message, from_email, [
                              to_email], html_message=html_message)
                except Exception as e:
                    print(f'Failed to send confirmation email: {e}')

                messages.success(
                    request, 'Payment successful! Your application has been submitted.')
                return redirect('applications:license-confirmation', application_id=dl_app.id)
        except Service.DoesNotExist:
            messages.error(request, 'Service not found.')
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')

    svc = Service.objects.filter(name__icontains='driver').first()
    if not svc:
        svc = None
    context = {'title': 'Payment', 'application': dl_app,
               'service': svc, 'amount': svc.base_fee if svc else Decimal('0.00')}
    return render(request, 'applications/passport_payment.html', context)


@login_required
def drivers_license_confirmation(request, application_id):
    dl_app = get_object_or_404(
        DriversLicenseApplication, id=application_id, user=request.user)
    payment = Payment.objects.filter(
        drivers_license_application=dl_app).first()
    app_data = request.session.get('drivers_license_app_data', {})
    return render(request, 'applications/passport_confirmation.html', {'title': 'Confirmation', 'passport_app': dl_app, 'payment': payment, 'app_data': app_data})
