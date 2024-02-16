from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from user.models import Employee


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Employee.objects.filter(level__in=[1, 2])


class EmployeesListView(ListView):
    model = Employee
    template_name = 'employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Employee.objects.all()


def load_hierarchy(request, employee_id):
    # Отримати дані для обраного співробітника (employee_id) та його підлеглих
    supervisor = Employee.objects.get(id=employee_id)
    subordinates = Employee.objects.filter(supervisor=supervisor)

    # Підготовити дані для відправки у форматі JSON
    data = {
        'supervisor': {'id': supervisor.id, 'name': supervisor.full_name},
        'subordinates': [{'id': sub.id, 'name': sub.full_name} for sub in subordinates],
    }

    # Повернути дані у форматі JSON
    return JsonResponse(data, safe=False)
