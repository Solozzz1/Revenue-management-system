from django import forms
from .models import UserProfile, TaxType, TaxpayerCategory, BillType

class TaxTypeForm(forms.ModelForm):
    class Meta:
        model = TaxType
        fields = ['name', 'description', 'tax_rate', 'is_active']  # Include 'is_active' as it's relevant for management

class TaxpayerRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['id_number', 'physical_address', 'email', 'phone_number', 'business_name',
                  'business_registration_number', 'income_range', 'taxpayer_category']  # Ensure all fields are defined in the model

    def clean(self):
        cleaned_data = super().clean()
        id_number = cleaned_data.get("id_number")
        business_registration_number = cleaned_data.get("business_registration_number")
        business_name = cleaned_data.get("business_name")
        
        if not id_number and not business_registration_number:
            raise forms.ValidationError("Either an ID number (for individuals) or a Business Registration Number (for businesses) is required.")
        if business_registration_number and not business_name:
            raise forms.ValidationError("Business name is required if a Business Registration Number is provided.")
        
        return cleaned_data

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['business_name', 'business_registration_number', 'income_range', 'taxpayer_category']

class EditTaxpayerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['id_number', 'physical_address', 'email', 'phone_number', 
                  'business_name', 'business_registration_number', 'income_range', 'taxpayer_category']

class TaxpayerCategoryForm(forms.ModelForm):
    class Meta:
        model = TaxpayerCategory
        fields = ['name', 'description']

class BillTypeForm(forms.ModelForm):
    class Meta:
        model = BillType
        fields = ['name', 'description', 'is_active']  # Include 'is_active' as it's relevant for management
