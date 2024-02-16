from django.urls import path
from user.views import EmployeeListView, load_hierarchy, EmployeesListView, load_employee_list, UserSignInView, \
    UserLogoutView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='home'),
    path('load_hierarchy/<int:employee_id>/', load_hierarchy, name='load_hierarchy'),
    path('employees/', EmployeesListView.as_view(), name='employees'),
    path('load_employee_list/', load_employee_list, name='load_employee_list'),
    path("login/", UserSignInView.as_view(), name="sign-in"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
