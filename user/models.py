from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    hire_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['level']
