from django.core.exceptions import ValidationError
from django.db import models

from Base.models import Person
from members.utils.phone_validator import validate_phone_number


class MembersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('my_dependants')


class Member(Person):
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    objects = MembersManager()

    def save(self, *args, **kwargs):
        if not validate_phone_number(self.phone_number):
            raise ValidationError(
                f'The phone number {self.phone_number} is invalid')
        super().save(*args, **kwargs)
