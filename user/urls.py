from django.urls import path
from user.views import EmployeeListView, load_hierarchy, EmployeesListView, load_employee_list, UserSignInView, \
    UserLogoutView, ProfileView, ProfileUpdateView, ProfileDeleteView, ajax_supervisors

urlpatterns = [
    path('', EmployeeListView.as_view(), name='home'),
    path('load_hierarchy/<int:employee_id>/', load_hierarchy, name='load_hierarchy'),
    path('employees/', EmployeesListView.as_view(), name='employees'),
    path('load_employee_list/', load_employee_list, name='load_employee_list'),
    path("login/", UserSignInView.as_view(), name="sign-in"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path('employees/<int:pk>/update/', ProfileUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', ProfileDeleteView.as_view(), name='employee_delete'),
    path('ajax/supervisors/', ajax_supervisors, name='ajax_supervisors'),

]
