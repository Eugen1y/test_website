from django import forms

class EmployeeSortForm(forms.Form):
    SORT_CHOICES = (
        ('full_name', 'Full Name'),
        ('position', 'Position'),
        ('hire_date', 'Hire Date'),
        ('email', 'Email'),
        ('level', 'Level'),
    )

    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False, label='Sort by')
