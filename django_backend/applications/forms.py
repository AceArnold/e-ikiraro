from django import forms
from e_ikiraro.models import PassportApplication
from django.core.validators import FileExtensionValidator

class PassportApplicationForm(forms.ModelForm):
    # Personal Information
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    place_of_birth = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter place of birth'
        })
    )
    gender = forms.ChoiceField(
        choices=[('Male', 'Male'), ('Female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    nationality = forms.CharField(
        max_length=100,
        initial='Burundian',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nationality'
        })
    )
    
    # Contact Information
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+257 XX XXX XXX'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    current_address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter your current address'
        })
    )
    
    # Parent Information
    father_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Father's full name"
        })
    )
    mother_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Mother's full name"
        })
    )
    
    # Emergency Contact
    emergency_contact_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Emergency contact name'
        })
    )
    emergency_contact_phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Emergency contact phone'
        })
    )
    
    # Previous Passport Information (Optional)
    previous_passport_number = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Previous passport number (if any)'
        })
    )
    previous_passport_issue_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


    passport_photo = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png'
        }),
        help_text='Upload a recent passport-sized photo (JPEG/PNG, max 5MB)'
    )
    birth_certificate = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'application/pdf,image/jpeg,image/png'
        }),
        help_text='Upload your birth certificate (PDF/Image, max 5MB)'
    )
    national_id = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'application/pdf,image/jpeg,image/png'
        }),
        help_text='Upload your national ID (PDF/Image, max 5MB)'
    )

    class Meta:
        model = PassportApplication
        fields = [
            'passport_type',
            'first_name', 'last_name', 'date_of_birth', 'place_of_birth', 'gender', 'nationality',
            'phone_number', 'email', 'current_address',
            'father_name', 'mother_name', 'emergency_contact_name', 'emergency_contact_phone',
            'previous_passport_number', 'previous_passport_issue_date',
            'passport_photo', 'birth_certificate', 'national_id',
        ]
        widgets = {
            'passport_type': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter place of birth'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationality'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+257 XX XXX XXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'current_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your current address'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's full name"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's full name"}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact phone'}),
            'previous_passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Previous passport number (if any)'}),
            'previous_passport_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nationality'].initial = 'Burundian'

    def clean_passport_photo(self):
        photo = self.cleaned_data.get('passport_photo')
        if photo:
            if photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('Photo file size must be under 5MB')
        return photo

    def clean_birth_certificate(self):
        cert = self.cleaned_data.get('birth_certificate')
        if cert:
            if cert.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 5MB')
        return cert

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id:
            if national_id.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must be under 5MB')
        return national_id