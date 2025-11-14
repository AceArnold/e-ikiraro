from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Crispy forms imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class OTPVerificationForm(forms.Form):
    code = forms.CharField(max_length=6, required=True,
                           widget=forms.TextInput(attrs={'placeholder':'Enter verification code','autocomplete':'off'}))



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Widget attributes: keep Django names but set IDs/placeholders that
        # match the frontend static HTML so existing JS/CSS works unchanged.
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'fullname',
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'Enter your email'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Enter a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'confirmPassword',
            'placeholder': 'Confirm your password'
        })

        # Crispy helper with explicit Layout so {{ form|crispy }} outputs
        # the exact structure we want. We include the submit here so the
        # template no longer needs a manual submit button.
        # self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.layout = Layout(
        #     Div(
        #         Field('username'),
        #         css_class='mb-3'
        #     ),
        #     Div(
        #         Field('email'),
        #         css_class='mb-3'
        #     ),
        #     Div(
        #         Field('password1'),
        #         css_class='mb-3'
        #     ),
        #     Div(
        #         Field('password2'),
        #         css_class='mb-3'
        #     ),
        #     Div(Submit('submit', 'Sign Up',
        #         css_class='btn btn-primary'), css_class='mt-2')
        # )

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user 
