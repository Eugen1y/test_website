from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(LoginRequiredMixin):
    login_url = "/login/"