from django import forms
from django.contrib.auth.forms import AuthenticationForm


class EmployeeSortForm(forms.Form):
    SORT_CHOICES = (
        ('', ''),
        ('full_name', 'Full Name'),
        ('position', 'Position'),
        ('hire_date', 'Hire Date'),
        ('email', 'Email'),
        ('level', 'Level'),
    )

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Sort by')
    search_query = forms.CharField(max_length=255, required=False, label='Search')



class SignInForm(AuthenticationForm):
    pass
