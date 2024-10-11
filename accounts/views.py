from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, ForgotPasswordForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import password_validation  # Import password validation
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .forms import *
from django.contrib.auth import update_session_auth_hash  # Import this
from django.utils import timezone

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard or another page
            else:
                form.add_error(None, 'Invalid username or password')  # Custom error message
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def signup_view(request):
    """Handle user signup."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login_view')  # Redirect to the login page
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def forgot_password(request):
    """Handle password reset request."""
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(reverse('reset_password', args=[uid, token]))

          
                send_mail(
                    'Password Reset Request',
                    f'Click the link to reset your password: {reset_link}',
                    'jayarora3100@gmail.com',  # Update with your sender email
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Reset instructions have been sent to your email.')
            except User.DoesNotExist:
                messages.error(request, 'Email address not found.')
            return redirect('forgot_password')  # Redirect to the same page or another page
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot.html', {'form': form})
    


def reset_password(request, uidb64, token):
    """Handle password reset using the token and uid."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)

            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.last_updated = timezone.now()
                user.save()

                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('login_view')  # Redirect to the login page
            else:
                for error in form.errors.values():
                    messages.error(request, ' '.join(error))

        else:
            form = ResetPasswordForm()

        return render(request, 'reset_password.html', {'form': form, 'uidb64': uidb64, 'token': token})

    else:
        messages.error(request, 'Invalid password reset link.')
        return redirect('forgot_password')
    
@login_required(login_url='/login/')
def dashboard_view(request):
    """Handle user dashboard view."""
    return render(request, 'dashboard.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('login_view')


@login_required(login_url='/login/')
def profile_view(request):
    return render(request, 'Profile.html')


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user=form.save(commit=False) 
            user.last_updated=timezone.now()
            user.save()

            # Log the user out after password change
            update_session_auth_hash(request, user)  # Important! Keep the user logged in.
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})