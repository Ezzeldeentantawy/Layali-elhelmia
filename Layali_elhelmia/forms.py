from django import forms
from .models import Meals , Kind , Category , Users 
from django.urls import reverse
from django.core.validators import RegexValidator




class MealsForm(forms.ModelForm):
    class Meta:
        model = Meals
        fields = '__all__'
        widgets = {
            'description_in_arabic': forms.Textarea(attrs={'rows': 2 , 'columns': 2}),
            'description_in_english': forms.Textarea(attrs={'rows': 2 , 'columns': 2})

        }
class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username' , 'city' , 'phone_number','street_name','email','home_num']
    username = forms.CharField(max_length=35)
    city = forms.CharField(max_length=35)
    phone_number = forms.CharField(max_length=15,
    validators=[# to check if phone number is valid
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ])
    street_name = forms.CharField(max_length=35)
    email = forms.EmailField()
    home_num = forms.IntegerField()