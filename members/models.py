from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from Base.models import Person
from members.utils.phone_validator import validate_phone_number


class MembersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'my_dependants')


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

    @property
    def contributions(self):
        return self.member_contributions.all()

    @property
    def total_contributions(self):
        _total_contributions = self.member_contributions.aggregate(
            models.Sum('amount'))

        return _total_contributions

    @property
    def paid_up(self):
        today = datetime.now()
        current_month = today.strftime("%B")
        return self.member_contributions.filter(month=current_month).exists()

    def __str__(self):
        return f'{self.first_name}'


class Dependant(Person):
    SPOUSE, CHILD = 'Spouse', 'Child'

    DEPENDANT_TYPES = [
        (SPOUSE, 'Spouse'),
        (CHILD, 'Child')
        ]

    principal_member = models.ForeignKey(
        Member, related_name='my_dependants', on_delete=models.CASCADE)
    relationship = models.CharField(choices=DEPENDANT_TYPES, max_length=15)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.relationship} : {self.first_name}' # noqa
