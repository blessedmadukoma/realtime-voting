from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Voter
from django.db import transaction


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")
    phone = forms.CharField(max_length=15, label="Phone Number:")
    birth_date = forms.DateField(label="Birth Date: (YYYY-MM-DD)")
    address = forms.CharField(max_length=200, label="Home Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State")
    zipcode = forms.CharField(max_length=8, label="Zip Code")
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")

    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'username',
                  'email', 'birth_date', 'phone', 'address', 'city', 'state', 'zipcode', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class VoterUserForm(forms.ModelForm):
    class Meta:
        model = Voter
        exclude = ('json', 'user')
        # fields = ('phone', 'address', 'city', 'state', 'zipcode')

        # labels = {
        #     'phone': 'Phone Number',
        #     'address': 'Address',
        #     'city': 'City',
        #     'state': 'State',
        #     'zipcode': 'Zip Code',
        # }

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        # user.phone = self.cleaned_data['phone']
        # user.address = self.cleaned_data['address']
        # user.city = self.cleaned_data['city']
        # user.state = self.cleaned_data['state']
        if commit:
            user.save()
        return user
