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

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render(self.request, 'employee_list_partial.html', context).content.decode('utf-8')
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


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


def load_employee_list(request, search_query=None):
    # Получить список пользователей по заданному поисковому запросу
    if search_query:
        employees = Employee.objects.filter(
            Q(full_name__icontains=search_query) |
            Q(position__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(hire_date__icontains=search_query) |
            Q(level__icontains=search_query)
        ).order_by('full_name')
    else:
        employees = Employee.objects.all()

    # Подготовить данные для возврата в формате JSON
    data = {
        'employees': [{'id': emp.id, 'name': emp.full_name, 'position': emp.position, 'email': emp.email} for emp in employees],
    }

    # Вернуть данные в формате JSON
    return JsonResponse(data, safe=False)
