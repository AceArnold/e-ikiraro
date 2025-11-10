from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(
                f"User '{user.username}' created successfully with ID: {user.id}")
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('e-ikiraro-home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html', {'title': 'Login'})
