import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import get_user_model
from django.conf import settings
from .models import CustomUser
from employeer.models import EmployerProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pyotp
import qrcode
import re

CustomUser = get_user_model()

# Define password policy constants
MIN_PASSWORD_LENGTH = 8
REQUIRES_UPPERCASE = True
REQUIRES_NUMBER = True
REQUIRES_SPECIAL_CHAR = True

def generate_otp(user):
    if not user.mfa_secret:
        user.mfa_secret = pyotp.random_base32()
        user.save()
    otp_uri = pyotp.totp.TOTP(user.mfa_secret).provisioning_uri(
        name=user.email,
        issuer_name="Employment Placement App"
    )
    qr = qrcode.make(otp_uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)  
    qr_code = base64.b64encode(buffer.getvalue()).decode("utf-8")
    qr_code_data_uri = f"data:image/png;base64,{qr_code}"

    return qr_code_data_uri

def verify_2fa_otp(user, otp):
    totp = pyotp.TOTP(user.mfa_secret)
    if totp.verify(otp):
        user.mfa_enabled = True
        user.save()

        return True

    return False

def home_view(request):
    return render(request, 'home.html')

@login_required
def profile_view(request):
    user = request.user

    # Ensure user is an instance of CustomUser
    if not isinstance(user, CustomUser):
        return HttpResponseForbidden("Invalid user.")

    # Require MFA before allowing profile access/creation
    if not user.mfa_enabled:
        request.session['mfa_user_id'] = user.id
        messages.warning(request, 'You must activate Two-Factor Authentication before creating your profile.')
        return redirect('activate_mfa')

    user = request.user
    if user.user_type == '2':
        if not hasattr(user, 'employer_profile'):
            return redirect('create_employer_profile')
        else:
           return redirect('employer_dashboard')
    elif user.user_type == '1':
        if not hasattr(user, 'jobseekerprofile'):
            return redirect('create_jobseeker_profile')
    qr_code_data_uri = generate_otp(user)
    is_employer = hasattr(user, 'employerprofile')

    return render(request, 'profile.html', {"qrcode": qr_code_data_uri})

def activate_mfa(request):
    user_id = request.session.get('mfa_user_id')
    if not user_id:
        return redirect('error')
    user = get_object_or_404(CustomUser, id=user_id)
    qr_code_data_uri = generate_otp(user)

    return render(request, 'otp_activate.html', {"qrcode": qr_code_data_uri, "user_id_mfa": user_id})

def verify_mfa(request):
    if request.method == 'POST':
        otp = request.POST.get('otp_code')
        user_id = request.POST.get('user_id')
        if not user_id:
            messages.error(request, 'Invalid parameters. Please try again.')

            return render(request,'otp_verify.html', {'user_id': user_id})
        user = get_object_or_404(CustomUser, id=user_id)
        if verify_2fa_otp(user, otp):
            if request.user.is_authenticated:
                messages.success(request, '2FA enabled successfully !')

                return redirect('profile')
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('profile')
        else:
            if request.user.is_authenticated:
                messages.error(request, 'Invalid OTP code. Please try again.')

                return redirect('profile')
            messages.error(request, 'Invalid OTP code. Please try again.')

            return render(request,'otp_verify.html', {'user_id': user_id})
       
    return render(request,'otp_verify.html', {'user_id': user_id})

@login_required
def disable_2fa(request):
    user = request.user
    if user.mfa_enabled:
        user.mfa_enabled = False
        user.save()
        messages.success(request, "Two-Factor Authentication has been disabled.")
 
        return redirect('profile')
    else:
        messages.info(request, "2FA is already disabled.")

    return redirect('profile')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.mfa_enabled:

                return render(request,'otp_verify.html', {'user_id': user.id})
            login(request, user)
            messages.success(request, 'Login successful!')

            return redirect('profile') 
        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request,'login.html')

@login_required
def logout_page(request):
    logout(request)  
    messages.success(request, 'You have been logged out successfully.') 

    return redirect('/')


def signup_view(request, user_type):
    """Handles new user registration with password policy enforcement."""
    context = {
        'user_type': user_type
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1') # Use 'password' for consistency
        password2 = request.POST.get('password2')

        # 1. Check if passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'signup.html', context)

        # 2. Enforce password policy
        if len(password) < MIN_PASSWORD_LENGTH:
            messages.error(request, f'Password must be at least {MIN_PASSWORD_LENGTH} characters long.')
            return render(request, 'signup.html', context)

        if REQUIRES_UPPERCASE and not re.search(r"[A-Z]", password):
            messages.error(request, 'Password must contain at least one capital letter.')
            return render(request, 'signup.html', context)

        if REQUIRES_NUMBER and not re.search(r"[0-9]", password):
            messages.error(request, 'Password must contain at least one number.')
            return render(request, 'signup.html', context)

        # Special characters: using a common set. You can customize this regex.
        # r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]" covers many common special chars
        if REQUIRES_SPECIAL_CHAR and not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            messages.error(request, 'Password must contain at least one special character (e.g., !@#$%^&*).')
            return render(request, 'signup.html', context)

        # 3. Check if email is already taken
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please try another.')
            return render(request, 'signup.html', context)

        # 4. Create the new user
        # Note: Setting mfa_enabled=True directly upon creation.
        # It's usually better to have the user activate it themselves after signup.
        # However, following your original logic to proceed to activate_mfa.
        user = CustomUser.objects.create_user(username=email, email=email, password=password, mfa_enabled=False, user_type=user_type)
        user.save()
        messages.success(request, 'Sign up successful! Please activate Two-Factor Authentication for your account.')
        request.session['mfa_user_id'] = user.id

        return redirect('activate_mfa')

    return render(request, 'signup.html', context)

def privacy_policy(request):
    return render(request, 'privacy_cookies_policy.html')

def account_delete_procedure(request):
    return render(request, 'account_delete_procedure.html')