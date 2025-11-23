from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from datetime import timedelta

from .forms import UserRegisterForm, OTPVerificationForm
from .tokens import account_activation_token
from .models import EmailOTP

import random

OTP_EXPIRY_MINUTES = 8


def _generate_otp():
    return f"{random.randint(100000, 999999):06d}"


def _send_otp_email(request, user, to_email, otp_code):
    subject = 'Your E-ikiraro verification code'
    html_content = render_to_string('users/otp_email.html', {
        'user': user.username,
        'code': otp_code,
        'expires_minutes': OTP_EXPIRY_MINUTES
    })
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
    email.attach_alternative(html_content, 'text/html')
    email.send()


def register(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # creating OTP
            code = _generate_otp()
            expires = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
            EmailOTP.objects.create(user=user, code=code, expires_at=expires)

            # send OTP email
            _send_otp_email(
                request, user, form.cleaned_data.get('email'), code)

            print(
                f"User '{user.username}' created successfully with ID: {user.id}")
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}! A verification code was sent to your email.')
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            return redirect('verify-otp', uidb64=uidb64)
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form, 'title': 'Register-E-ikiraro'},)


def logout_view(request):
    logout(request)
    return redirect('e-ikiraro-home')


def verify_otp(request, uidb64):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        messages.error(request, 'Invalid verification link.')
        return redirect('register')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip()
            otp_qs = EmailOTP.objects.filter(
                user=user, code=code, used=False).order_by('-created_at')
            otp = otp_qs.first() if otp_qs.exists() else None
            if otp and otp.is_valid():
                user.is_active = True
                user.save()
                otp.mark_used()
                messages.success(
                    request, 'Your account has been activated. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid or expired code.')
    else:
        form = OTPVerificationForm()

    return render(request, 'users/verify_otp.html', {
        'form': form,
        'user': user,
        'uidb64': uidb64,
        'expires_minutes': OTP_EXPIRY_MINUTES,
    })


def resend_otp(request, uidb64):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        messages.error(request, 'Invalid reqeust.')
        return redirect('register')

     # invalidate previous OTPs and create new
    EmailOTP.objects.filter(user=user, used=False).update(used=True)
    code = _generate_otp()
    expires = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
    EmailOTP.objects.create(user=user, code=code, expires_at=expires)
    _send_otp_email(request, user, user.email, code)

    messages.success(
        request, 'A new verification code was sent to your email.')
    return redirect('verify-otp', uidb64=uidb64)


@login_required
def profile(request):
    return render(request, 'users/profile_new.html', {'title': 'Profile'})
