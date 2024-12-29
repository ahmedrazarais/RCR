from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TeacherProfile, StudentProfile
from django import forms
from django.contrib.auth import get_user_model, authenticate


class CustomSignupForm(UserCreationForm):
    """
    Combined signup form for both Teachers and Students.
    Fields are displayed dynamically based on the user status (teacher/student).
    """

    section = forms.CharField(max_length=20, required=False, label="Section")
    roll_number = forms.CharField(max_length=20, required=False, label="Roll Number")
    recovery_email = forms.EmailField(required=True, label="Recovery Email")  # Add recovery_email field

    class Meta:
        model = User
        fields = ["username", "email", "recovery_email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """
        Dynamically adjust fields based on the 'status' passed from the view.
        """
        self.status = kwargs.pop('status', None)  # Pop status from kwargs
        super().__init__(*args, **kwargs)

        if self.status == 'teacher':
            # Show fields specific to teachers
       
            self.fields.pop('section')
            self.fields.pop('roll_number')
        elif self.status == 'student':
            # Show fields specific to students
            self.fields['section'].required = True
            self.fields['roll_number'].required = True
            

    def save(self, commit=True):
        """
        Save the user and their profile based on the selected status.
        """
        user = super().save(commit=False)
        user.status = self.status
        user.recovery_email = self.cleaned_data['recovery_email']  # Save recovery_email
        if commit:
            user.save()
            if self.status == 'teacher':
                TeacherProfile.objects.create(
                    user=user,
                    
                )
            elif self.status == 'student':
                StudentProfile.objects.create(
                    user=user,
                    section=self.cleaned_data['section'],
                    roll_number=self.cleaned_data['roll_number']
                )
        return user





class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                # Add an error specific to the password field
                self.add_error('password', "Invalid password. Please try again.")
        return cleaned_data






class RecoveryForm(forms.Form):
    """
    Form to input recovery email address for account recovery.
    """
    recovery_email = forms.EmailField(label="Recovery Email", required=True)

    def clean_recovery_email(self):
        recovery_email = self.cleaned_data.get('recovery_email')
        User = get_user_model()

        # Check if the recovery email exists in the database
        if not User.objects.filter(recovery_email=recovery_email).exists():
            raise forms.ValidationError("The recovery email address does not exist in our records.")
        return recovery_email



class SetNewEmailForm(forms.Form):
    """
    Form to set a new email address after recovery email verification.
    """
    new_email = forms.EmailField(label="New Email", required=True)
    confirm_email = forms.EmailField(label="Confirm Email", required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get("new_email")
        confirm_email = cleaned_data.get("confirm_email")

        if new_email != confirm_email:
            raise forms.ValidationError("The new email addresses do not match.")

        return cleaned_data



class SetNewPasswordForm(forms.Form):
    """
    Form to set a new password after recovery email verification.
    """
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")

        # Additional password validation logic (e.g., minimum length, complexity)
        if new_password is None or len(new_password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return cleaned_data
