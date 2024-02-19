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
    """View to display a list of employees."""
    model = Employee
    template_name = 'employee.html'
    context_object_name = 'page_obj'

    def get_queryset(self):
        return Employee.objects.filter(level__in=[1, 2])


class EmployeesListView(ListView):
    """View to display a list of employees with sorting and searching options."""
    model = Employee
    template_name = 'employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        """Override queryset to filter, sort, and search employees."""
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
        """Add the EmployeeSortForm to the context."""
        context = super().get_context_data(**kwargs)
        context['form'] = EmployeeSortForm(self.request.GET)
        return context

    def render_to_response(self, context, **response_kwargs):
        """Render the view and support Ajax rendering."""
        if self.request.is_ajax():
            html = render(self.request, 'employee_list_partial.html', context).content.decode('utf-8')
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


def load_hierarchy(request, employee_id):
    """Load the hierarchical structure of employees for a specific supervisor."""
    supervisor = Employee.objects.get(id=employee_id)
    subordinates = Employee.objects.filter(supervisor=supervisor)

    data = {
        'supervisor': {'id': supervisor.id, 'name': supervisor.full_name},
        'subordinates': [{'id': sub.id, 'name': sub.full_name, 'subordinates_count': len(sub.employee_set.all())} for
                         sub in subordinates],
    }

    return JsonResponse(data, safe=False)


def load_employee_list(request, search_query=None):
    """Load the list of employees based on the search query."""
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

    data = {
        'employees': [{'id': emp.id, 'name': emp.full_name, 'position': emp.position, 'email': emp.email} for emp in
                      employees],
    }

    return JsonResponse(data, safe=False)


class UserSignInView(LoginView):
    """User sign-in views implementation"""
    form_class = SignInForm
    template_name = 'sign-in.html'

    def get_success_url(self):
        """Get the URL to redirect to upon successful login."""
        return reverse_lazy('home')


class UserLogoutView(RedirectView):
    """User logout views implementation"""

    def get_redirect_url(self, *args, **kwargs):
        """Get the URL to redirect to upon logout."""
        return reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        """Handle user logout."""
        logout(request)
        return super(UserLogoutView, self).get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, DetailView):
    """View to display user profile information."""
    model = Employee
    template_name = 'profile.html'
    context_object_name = 'employee'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update user profile information."""
    model = Employee
    template_name = 'employee_form.html'
    form_class = EmployeeForm

    def get_success_url(self):
        """Get the URL to redirect to upon successful profile update."""
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete user profile."""
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('home')


def ajax_supervisors(request):
    """Load supervisors based on the selected level."""
    selected_level = request.GET.get('level', None)
    selected_level = int(selected_level) - 1
    supervisors = Employee.objects.filter(level=selected_level).values('id', 'full_name').exclude(
        full_name=request.user.full_name)

    return JsonResponse(list(supervisors), safe=False)
