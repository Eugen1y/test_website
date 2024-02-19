import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from user.models import Employee


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


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'hire_date', 'email', 'supervisor', 'level']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

        # Отримати унікальні рівні
        levels = Employee.objects.exclude(level=None).values_list('level', flat=True).distinct()

        # Створити кортеж для варіантів у вигляді (value, display)
        level_choices = [(level, level) for level in levels]

        # Встановити варіанти для поля level
        self.fields['level'] = forms.ChoiceField(choices=level_choices,
                                                 widget=forms.Select(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        employees = self.instance.employee_set.all()
        if self.instance.employee_set.all():
            supervisor = Employee.objects.get(pk=self.instance.pk).supervisor
            new_supervisor = random.choice(Employee.objects.filter(supervisor=supervisor).exclude(pk=self.instance.pk))
            for employee in employees:
                employee.supervisor = new_supervisor
                employee.save()
        return super(EmployeeForm, self).save()
