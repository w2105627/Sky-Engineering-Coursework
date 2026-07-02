# Author : w2105627
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.models import Employee


class ProfileForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True, label='Full Name')
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        employee = getattr(self.user, 'employee_profile', None)
        self.fields['full_name'].initial = employee.full_name if employee else ''
        self.fields['username'].initial = self.user.username
        self.fields['email'].initial = self.user.email

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError('That username is already taken.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError('That email is already registered.')

        return email

    def save(self):
        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save()

        try:
            employee = Employee.objects.get(user=self.user)
            employee.full_name = self.cleaned_data['full_name']
            employee.save()
        except Employee.DoesNotExist:
            Employee.objects.create(
                user=self.user,
                full_name=self.cleaned_data['full_name'],
            )

        return self.user


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label='Full Name')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('That email is already registered.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            Employee.create_for_user(user, self.cleaned_data['full_name'])

        return user
