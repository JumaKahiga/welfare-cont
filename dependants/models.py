from django.db import models

from Base.models import Person
from members.models import Member


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
