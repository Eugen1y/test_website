from django.urls import path
from user.views import EmployeeListView, load_hierarchy

urlpatterns = [
    path('', EmployeeListView.as_view(), name='user'),
    path('load_hierarchy/<int:employee_id>/', load_hierarchy, name='load_hierarchy'),

]
