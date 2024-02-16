from django.urls import path
from user.views import EmployeeListView, load_hierarchy, EmployeesListView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee'),
    path('load_hierarchy/<int:employee_id>/', load_hierarchy, name='load_hierarchy'),
    path('employees/', EmployeesListView.as_view(), name='employees'),
]
