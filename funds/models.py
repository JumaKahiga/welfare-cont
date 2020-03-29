from django.core.exceptions import ValidationError
from django.db import models

from members.models import Member


class Contribution(models.Model):
    JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE =\
        'January', 'February', 'March', 'April', 'May', 'June'

    JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER =\
        'July', 'August', 'September', 'October', 'November', 'December'

    MONTHS = [
        (JANUARY, 'January'),
        (FEBRUARY, 'February'),
        (MARCH, 'March'),
        (APRIL, 'April'),
        (MAY, 'May'),
        (JUNE, 'June'),
        (JULY, 'July'),
        (AUGUST, 'August'),
        (SEPTEMBER, 'September'),
        (OCTOBER, 'October'),
        (NOVEMBER, 'November'),
        (DECEMBER, 'December')]

    member = models.ForeignKey(
        Member, related_name='member_contributions', on_delete=models.CASCADE)
    month = models.CharField(choices=MONTHS, max_length=20)
    amount = models.PositiveIntegerField(default=250)
    payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)

    def total_funds_contributed(self):
        return self.objects.aggregate(models.Sum('amount'))

    def available_funds(self):
        collected = self.objects.aggregate(models.Sum('amount'))
        disbursed = Disbursement.objects.aggregate(models.Sum('amount'))

        return (collected - disbursed)


class Disbursement(models.Model):
    member = models.ForeignKey(
        Member, related_name='member_disbursements', on_delete=models.CASCADE)

    authorized_by = models.ForeignKey(
        Member, related_name='member_authorizations',
        null=True, on_delete=models.PROTECT)

    disbursement_date = models.DateField()
    amount = models.PositiveIntegerField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.approved and not self.authorized_by:
            raise ValidationError(
                'Authorizing member has to be provided before disbursement is approved') # noqa

        if self.approved and not self.authorized_by.is_active:
            raise ValidationError(
                'Disbursements can only be approved by active members') # noqa

        if not self.member.is_active:
            raise ValidationError(
                'Disbursements can only be done for active members') # noqa

    def total_funds_disbursed(self):
        return self.objects.aggregate(models.Sum('amount'))
