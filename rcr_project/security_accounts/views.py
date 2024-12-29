from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, RecoveryForm, SetNewEmailForm , SetNewPasswordForm


from .forms import CustomSignupForm

def signup_home(request, user_type):
    """
    Handle signup for both teacher and student based on the 'user_type'.
    Renders the form with fields depending on the selected role.
    """

    
    if request.method == 'POST':
        # Pass user_type to dynamically configure the form
        form = CustomSignupForm(request.POST, status=user_type)
        if form.is_valid():
            form.save()  # Save the user and profile data
            
            return redirect('rcr_home')  # Redirect to login page after successful signup
    else:
        # Prepopulate the form with user_type as the status
        form = CustomSignupForm(status=user_type)

    # Render the signup page, passing the form and user_type context
    return render(request, 'security_accounts/signup_home.html', {
        'form': form,
        'usertype': user_type,
    })



def login_home(request, user_type):
    """
    Handle login for both teacher and student based on the 'user_type'.
    Authenticates the user and logs them in if credentials are correct.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if hasattr(user, 'status') and user.status == user_type:
                    login(request, user)
                    messages.success(request, f"Welcome, {user.username}! Logged in as {user_type}.")
                    return redirect('rcr_home')
                else:
                    messages.error(request, f"You don't have permission to log in as a {user_type}.")
            else:
                messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm()

    return render(request, 'security_accounts/login_home.html', {
        'form': form,
        'usertype': user_type,
    })









def logout(request):
    auth_logout(request)  # Log out the user
    messages.success(request, "You have successfully logged out.")
    return redirect('rcr_home')  # Correctly redirect to 'rcr_home'



def accounts_setting_home(request):
    return render(request,"security_accounts/Accounts_setting.html")





from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def recovery_view(request,update_type):
    """
    Handle the recovery form submission.
    """
    
    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        if form.is_valid():
            recovery_email = form.cleaned_data['recovery_email']
            # Store the email in the session for the next step
            request.session['recovery_email'] = recovery_email
            messages.success(request, "Recovery email verified successfully!")
            if update_type=="email":
                return redirect('accounts_set_new_email')  # Redirect to the next step
            else:
                return redirect('accounts_set_new_password')  # Redirect to the next step
    else:
        form = RecoveryForm()

    return render(request, 'security_accounts/recovery_form.html', {'form': form})




def set_new_email_view(request):
    if 'recovery_email' not in request.session:
        messages.error(request, "Invalid recovery session. Please try again.")
        return redirect('recovery_view')

    if request.method == 'POST':
        form = SetNewEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            recovery_email = request.session['recovery_email']

            # Check if the email already exists
            if User.objects.filter(email=new_email).exists():
                messages.error(request, "This email is already in use. Please use a different email.")
                return render(request, 'security_accounts/set_new_email_form.html', {'form': form})
            
            try:
                # Update the user's email
                user = User.objects.get(recovery_email=recovery_email)
                user.email = new_email
                user.save()

                # Clear the session and notify the user
                del request.session['recovery_email']
                messages.success(request, "Your email has been successfully updated.")
                return redirect('rcr_home')
            except User.DoesNotExist:
                messages.error(request, "User not found. Please try again.")
                return redirect('recovery_view')
    else:
        form = SetNewEmailForm()
    return render(request, 'security_accounts/set_new_email_form.html', {'form': form})





from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def set_new_password_view(request):
    """
    Handle setting a new password after recovery email verification.
    """
    if 'recovery_email' not in request.session:
        messages.error(request, "Invalid recovery session. Please try again.")
        return redirect('recovery_view')

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            recovery_email = request.session['recovery_email']

            try:
                # Retrieve the user using the recovery email
                user = User.objects.get(recovery_email=recovery_email)
                
                # Set the new password
                user.set_password(new_password)
                user.save()

                # Clear the session
                del request.session['recovery_email']

                # Optionally, log the user in after password change
                update_session_auth_hash(request, user)

                messages.success(request, "Your password has been successfully updated.")
                return redirect('rcr_home')
            except User.DoesNotExist:
                messages.error(request, "User not found. Please try again.")
                return redirect('recovery_view')
    else:
        form = SetNewPasswordForm()

    return render(request, 'security_accounts/set_new_password_form.html', {'form': form})








