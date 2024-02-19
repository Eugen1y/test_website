from django.contrib.auth.models import AbstractUser
from django.db import models

class Employee(AbstractUser):
    """
    Custom user model representing an employee in the organization.

    Attributes:
        full_name (str): The full name of the employee.
        position (str): The position or job title of the employee.
        hire_date (Date): The date when the employee was hired.
        supervisor (Employee): The supervisor of the employee, represented as a foreign key to itself.
        level (int): The level or hierarchy position of the employee.

    Methods:
        __str__: Returns the full name of the employee when the object is converted to a string.

    Meta:
        ordering: Orders the employees based on their hierarchy level.
    """

    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    hire_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """Return the full name of the employee when the object is converted to a string."""
        return self.full_name

    class Meta:
        """Meta options for the Employee model."""
        ordering = ['level']