from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from user.models import Employee
from .forms import EmployeeSortForm
from django.db.models import Q


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
        form = EmployeeSortForm(self.request.GET)
        if form.is_valid():
            sort_by = form.cleaned_data['sort_by']
            search_query = form.cleaned_data['search_query']
            queryset = Employee.objects.all()

            if search_query:
                queryset = queryset.filter(
                    Q(full_name__icontains=search_query) |
                    Q(position__icontains=search_query) |
                    Q(email__icontains=search_query) |
                    Q(hire_date__icontains=search_query) |
                    Q(level__icontains=search_query)

                ).order_by('full_name')

            if sort_by:
                queryset = queryset.order_by(sort_by)

            return queryset
        return Employee.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EmployeeSortForm(self.request.GET)
        return context


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


def employee_list(request):
    form = EmployeeSortForm(request.GET)

    if form.is_valid():
        sort_by = form.cleaned_data['sort_by']
        employees = Employee.objects.all().order_by(sort_by)
    else:
        employees = Employee.objects.all()

    return render(request, 'employees.html', {'employees': employees, 'form': form})
