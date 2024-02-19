from .mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from user.models import Employee
from .forms import EmployeeSortForm, SignInForm, EmployeeForm
from django.db.models import Q
from django.contrib.auth import logout


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
                ).order_by('full_name').exclude(is_superuser=True)

            if sort_by:
                queryset = queryset.order_by(sort_by).exclude(is_superuser=True)

            return queryset.exclude(is_superuser=True)
        return Employee.objects.exclude(is_superuser=True)

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
        'subordinates': [{'id': sub.id, 'name': sub.full_name,'subordinates_count':len(sub.employee_set.all())} for sub in subordinates],
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
        ).order_by('full_name').exclude(is_superuser=True)
    else:
        employees = Employee.objects.all().exclude(is_superuser=True)

    # Подготовить данные для возврата в формате JSON
    data = {
        'employees': [{'id': emp.id, 'name': emp.full_name, 'position': emp.position, 'email': emp.email} for emp in
                      employees],
    }

    # Вернуть данные в формате JSON
    return JsonResponse(data, safe=False)


class UserSignInView(LoginView):
    """User sign-in views implementation"""
    form_class = SignInForm
    template_name = 'sign-in.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(RedirectView):
    """User logout views implementation"""

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(UserLogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'profile.html'
    context_object_name = 'employee'



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employee_form.html'
    form_class = EmployeeForm

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})




class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('home')


def ajax_supervisors(request):
    selected_level = request.GET.get('level', None)
    selected_level = int(selected_level) - 1
    supervisors = Employee.objects.filter(level=selected_level).values('id', 'full_name').exclude(
        full_name=request.user.full_name)

    return JsonResponse(list(supervisors), safe=False)
