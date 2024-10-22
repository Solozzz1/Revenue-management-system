from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileUpdateForm, UserForm, RoleForm, AdminPasswordResetForm
from .models import User, Role
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)



# View for managing users (Admin access only)
@login_required
def manage_users(request):
    if not request.user.is_admin:
        return redirect('home')  # Redirect if not admin
    taxpayers = User.objects.filter(roles__name='taxpayer')
    return render(request, 'accounts/manage_users.html', {'users': taxpayers})

@login_required
def manage_roles(request):
    if not request.user.is_admin:
        return redirect('home')  # Redirect if not admin
    roles = Role.objects.all()
    return render(request, 'accounts/manage_roles.html', {'roles': roles})

# Registration view for new users
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign the taxpayer role by default
            taxpayer_role = Role.objects.get(name='taxpayer')
            user.roles.add(taxpayer_role)
            login(request, user)
            # Redirect to the taxpayer home page
            return redirect('taxpayer_home')  # Adjust this URL to your taxpayer dashboard/home page
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'accounts/login.html')

# Home page
def home(request):
    return render(request, 'accounts/home.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# User profile view and update
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()  # Save profile updates
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        elif password_form.is_valid():
            user = password_form.save(commit=False)
            user.set_password(password_form.cleaned_data['new_password1'])  # Ensure the password is hashed
            user.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = ProfileUpdateForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'password_form': password_form
    })

@login_required
def admin_reset_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminPasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'User password reset successfully!')
            return redirect('manage_users')
    else:
        form = AdminPasswordResetForm()

    return render(request, 'accounts/admin_reset_password.html', {'form': form, 'user': user})

# Admin-only view for creating users
@login_required
def user_create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'User created successfully!')
        return redirect('manage_users')
    return render(request, 'accounts/user_form.html', {'form': form})

# Admin-only view for editing users
@login_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, 'User updated successfully!')
        return redirect('manage_users')
    return render(request, 'accounts/user_form.html', {'form': form, 'user': user})

# Admin-only view for deleting users
@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('manage_users')
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})

# Admin-only view for creating roles
@login_required
def role_create(request):
    form = RoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Role created successfully!')
        return redirect('manage_roles')
    return render(request, 'accounts/role_form.html', {'form': form})

# Admin-only view for editing roles
@login_required
def role_edit(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    form = RoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        messages.success(request, 'Role updated successfully!')
        return redirect('manage_roles')
    return render(request, 'accounts/role_form.html', {'form': form, 'role': role})

# Admin-only view for deleting roles
@login_required
def role_delete(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    role.delete()
    messages.success(request, 'Role deleted successfully!')
    return redirect('manage_roles')

# Dashboard view for admin and auditor roles
def dashboard(request):
    if request.user.is_admin:
        return render(request, 'accounts/dashboard.html')
    return redirect('home')

# Accounts management (Admin and Taxpayer roles)
@login_required
def accounts(request):
    return render(request, 'accounts/accounts.html')

# Tax registration (Taxpayer role only)
@login_required
def tax_registration(request):
    return render(request, 'accounts/tax_registration.html')

# Revenue management (Admin and Taxpayer roles)
@login_required

def revenue_management(request):
    return render(request, 'accounts/revenue_management.html')
