from .utils import is_admin, is_taxpayer, role_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import TaxInvoice, TaxType, Payment, UserProfile, TaxpayerCategory, BillType
from .forms import TaxpayerRegistrationForm, BusinessRegistrationForm, TaxTypeForm, EditTaxpayerProfileForm, TaxpayerCategoryForm, BillTypeForm


@login_required
def generate_bill(request):
    user = request.user
    tax_type = TaxType.objects.filter(name="Income Tax", is_active=True).first()

    if not tax_type:
        messages.error(request, 'No active Income Tax type found. Please contact an administrator.')
        return redirect('error_page')

    bill_type = BillType.objects.filter(is_active=True).first()
    if not bill_type:
        messages.error(request, 'No active Bill Type found. Please contact an administrator.')
        return redirect('error_page')

    amount_due = calculate_tax(user)  # Ensure this function is defined
    invoice = TaxInvoice.objects.create(
        user=user,
        due_date=timezone.now() + timezone.timedelta(days=30),
        amount_due=amount_due,
        tax_type=tax_type,
        bill_type=bill_type
    )

    # Ensure that the email sending works properly
    try:
        send_mail(
            'New Tax Invoice',
            f'Your invoice {invoice.id} has been generated and is due by {invoice.due_date}.',
            'no-reply@taxsystem.com',
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        messages.error(request, f'Error sending email: {str(e)}')

    messages.success(request, f'Invoice {invoice.id} has been generated successfully!')
    return redirect('invoice_detail', invoice_id=invoice.id)

@login_required
def invoice_list(request):
    invoices = TaxInvoice.objects.filter(user=request.user)
    return render(request, 'tax/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(TaxInvoice, id=invoice_id, user=request.user)
    return render(request, 'tax/invoice_detail.html', {'invoice': invoice})

@login_required
def process_payment(request, invoice_id):
    invoice = get_object_or_404(TaxInvoice, id=invoice_id)

    if request.method == 'POST':
        try:
            amount_paid = float(request.POST['amount'])
            payment_ref = request.POST['payment_reference']
            payment_method = request.POST['payment_method']

            if amount_paid < invoice.amount_due:
                invoice.status = 'PP'
                invoice.amount_due -= amount_paid
            else:
                invoice.status = 'P'
                invoice.amount_due = 0
                invoice.is_paid = True

            Payment.objects.create(
                invoice=invoice,
                amount_paid=amount_paid,
                payment_reference=payment_ref,
                payment_method=payment_method
            )

            invoice.save()
            messages.success(request, 'Payment processed successfully!')
            return redirect('invoice_list')
        except ValueError:
            messages.error(request, 'Invalid amount. Please enter a valid number.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'tax/payment_form.html', {'invoice': invoice})

def view_taxpayer_history(request, taxpayer_id):
    taxpayer = get_object_or_404(TaxpayerProfile, id=taxpayer_id)
    # Assuming taxpayer has a related history model, retrieve the data
    history = taxpayer.history_set.all()  # Adjust this to your model setup
    return render(request, 'taxpayer_history.html', {'taxpayer': taxpayer, 'history': history})

@login_required
def manage_tax_types(request):
    if request.method == 'POST':
        form = TaxTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tax type created successfully.')
            return redirect('manage_tax_types')
    else:
        form = TaxTypeForm()

    tax_types = TaxType.objects.all()
    return render(request, 'tax/manage_tax_types.html', {'form': form, 'tax_types': tax_types})

@login_required
# Category Management Views

def manage_categories(request):
    categories = TaxpayerCategory.objects.all()
    return render(request, 'tax/manage_categories.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = TaxpayerCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Taxpayer Category created successfully!')
            return redirect('manage_categories')
    else:
        form = TaxpayerCategoryForm()
    return render(request, 'tax/category_form.html', {'form': form, 'title': 'Create Taxpayer Category'})

def category_edit(request, pk):
    category = get_object_or_404(TaxpayerCategory, pk=pk)
    if request.method == 'POST':
        form = TaxpayerCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Taxpayer Category updated successfully!')
            return redirect('manage_categories')
    else:
        form = TaxpayerCategoryForm(instance=category)
    return render(request, 'tax/category_form.html', {'form': form, 'title': 'Edit Taxpayer Category'})

def category_delete(request, pk):
    category = get_object_or_404(TaxpayerCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Taxpayer Category deleted successfully!')
        return redirect('manage_categories')
    return render(request, 'tax/category_confirm_delete.html', {'category': category})

# Bill Type Management Views

def manage_bill_types(request):
    bill_types = BillType.objects.all()
    return render(request, 'tax/manage_bill_types.html', {'bill_types': bill_types})

def bill_type_create(request):
    if request.method == 'POST':
        form = BillTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill Type created successfully!')
            return redirect('manage_bill_types')
    else:
        form = BillTypeForm()
    return render(request, 'tax/bill_type_form.html', {'form': form, 'title': 'Create Bill Type'})

def bill_type_edit(request, pk):
    bill_type = get_object_or_404(BillType, pk=pk)
    if request.method == 'POST':
        form = BillTypeForm(request.POST, instance=bill_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill Type updated successfully!')
            return redirect('manage_bill_types')
    else:
        form = BillTypeForm(instance=bill_type)
    return render(request, 'tax/bill_type_form.html', {'form': form, 'title': 'Edit Bill Type'})

def bill_type_delete(request, pk):
    bill_type = get_object_or_404(BillType, pk=pk)
    if request.method == 'POST':
        bill_type.delete()
        messages.success(request, 'Bill Type deleted successfully!')
        return redirect('manage_bill_types')
    return render(request, 'tax/bill_type_confirm_delete.html', {'bill_type': bill_type})

@login_required
def taxpayer_history(request):
    invoices = TaxInvoice.objects.filter(user=request.user)
    return render(request, 'tax/taxpayer_history.html', {'invoices': invoices})

# Taxpayer Profile Edit
@login_required
@role_required('taxpayer')
def edit_taxpayer_profile(request):
    
    profile = request.user.userprofile  # Assuming user has a profile
    if request.method == 'POST':
        form = EditTaxpayerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('taxpayer_profile_view', identifier=profile.id_number)
    else:
        form = EditTaxpayerProfileForm(instance=profile)
    return render(request, 'tax/edit_taxpayer_profile_template.html', {'form': form})

# Admin Full Management of Profiles
@user_passes_test(is_admin)
@login_required
def manage_taxpayer_profiles(request):
    profiles = UserProfile.objects.all()
    return render(request, 'tax/manage_taxpayer_profiles.html', {'profiles': profiles})

@user_passes_test(is_admin)
@login_required
def manage_system_features(request):
    # Logic for managing system features (add/remove settings or configurations)
    return render(request, 'tax/manage_system_features.html')

@login_required
def create_tax_type(request):
    if request.method == 'POST':
        form = TaxTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tax type created successfully.')
            return redirect('manage_tax_types')
    else:
        form = TaxTypeForm()

    return render(request, 'tax/create_tax_type.html', {'form': form})

@login_required
def edit_tax_type(request, tax_type_id):
    tax_type = get_object_or_404(TaxType, id=tax_type_id)

    if request.method == 'POST':
        form = TaxTypeForm(request.POST, instance=tax_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tax type updated successfully.')
            return redirect('manage_tax_types')
    else:
        form = TaxTypeForm(instance=tax_type)

    return render(request, 'tax/edit_tax_type.html', {'form': form})


def register_business_taxpayer(request):
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST)
        if form.is_valid():
            # Save the form or perform other logic
            return redirect('some_redirect_url')
    else:
        form = BusinessRegistrationForm()
    return render(request, 'tax/business_registration_template.html', {'form': form})
def register_individual_taxpayer(request):
    if request.method == 'POST':
        form = TaxpayerRegistrationForm(request.POST)
        if form.is_valid():
            # Save the form or perform other logic
            return redirect('some_redirect_url')
    else:
        form = TaxpayerRegistrationForm()
    return render(request, 'tax/registration_template.html', {'form': form})

@login_required
def delete_tax_type(request, tax_type_id):
    tax_type = get_object_or_404(TaxType, id=tax_type_id)
    tax_type.delete()
    messages.success(request, 'Tax type deleted successfully.')
    return redirect('manage_tax_types')


# Taxpayer Profile Access Logic
@login_required
def taxpayer_profile_view(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number', None)
        full_name = request.POST.get('full_name', None)
        business_name = request.POST.get('business_name', None)
        registration_number = request.POST.get('registration_number', None)

        if id_number and full_name:
            profile = get_object_or_404(UserProfile, id_number=id_number, user__full_name=full_name)
        elif business_name and registration_number:
            profile = get_object_or_404(UserProfile, business_registration_number=registration_number, business_name=business_name)
        else:
            messages.error(request, "Please provide valid credentials for profile access.")
            return redirect('taxpayer_profile_form')

        return render(request, 'tax/taxpayer_profile_template.html', {'profile': profile})
    
    return render(request, 'tax/taxpayer_profile_form.html')  # Form to input credentials
# Admin to manage tax payers

# Admin Manage Invoices
@user_passes_test(is_admin)
@login_required
def manage_invoices(request):
    invoices = TaxInvoice.objects.all()
    return render(request, 'tax/manage_invoices.html', {'invoices': invoices})


def revenue_report(request):
    # Your logic to generate a revenue report
    return render(request, 'tax/revenue_report_template.html')