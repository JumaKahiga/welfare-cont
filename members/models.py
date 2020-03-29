from django.db import models

from Base.models import Person


class Member(Person):
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
