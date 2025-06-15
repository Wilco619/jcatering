from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                  update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from .forms import (CustomAuthenticationForm, ProfileUpdateForm,
                     UserRegisterForm, UserUpdateForm)
from .utils import send_welcome_email


def auth_view(request):
    register_form = UserRegisterForm()
    login_form = CustomAuthenticationForm()
    return render(request, 'users/auth.html', {
        'register_form': register_form,
        'login_form': login_form
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email').lower()
            user.save()

            # Create or update profile
            profile = user.profile
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.save()

            # Log the user in
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # Send welcome email
            send_welcome_email(user)
            messages.success(request, 'Welcome to JAWAKA! Your account has been created successfully. Please check your email.')
            return redirect('japp:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return redirect('users:auth')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect admin users to admin dashboard
            if user.is_staff:
                return redirect('japp:admin_dashboard')
            return redirect('japp:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('users:auth')
    
    return redirect('users:auth')


@login_required
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('users:auth')