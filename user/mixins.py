from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin to require login for class-based views.

    If the user is not authenticated, they will be redirected to the login page.
    """

    login_url = "/login/"
