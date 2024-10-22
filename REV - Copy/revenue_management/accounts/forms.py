from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from .models import User, Role

# Registration form for new users
# Registration form for new users
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    phone_number = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)
    date_of_birth = forms.DateField(required=False)
    occupation = forms.CharField(max_length=255, required=False)
    company = forms.CharField(max_length=255, required=False)
    company_address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'phone_number', 
            'address', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'occupation', 
            'company', 
            'company_address', 
            'password1', 
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

# Form for updating user profile
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=True)  # Allow username change

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_picture']

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture and profile_picture.size > 1024 * 1024:
            raise forms.ValidationError('Profile picture must be less than 1MB')
        return profile_picture
    
# Form for creating and editing users
class UserForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'first_name', 'last_name', 'date_of_birth', 'occupation', 'company', 'company_address', 'roles']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']

class AdminPasswordResetForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data