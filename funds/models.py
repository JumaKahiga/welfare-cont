from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from members.models import Member


class Contribution(models.Model):
    now = datetime.now()
    current_year = now.year
    current_month = now.strftime("%B")
    current_period = {'month': current_month, 'year': current_year}

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
    year = models.PositiveIntegerField(default=current_year)
    amount = models.PositiveIntegerField(default=250)
    payment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.clean_fields()
        super().save(*args, **kwargs)

    def total_contribution(self):
        return Contribution.objects.aggregate(models.Sum('amount'))

    def total_monthly_contributions(self, month=current_month, year=current_year): # noqa
        monthly_contribution = Contribution.objects.filter(
            month=month, year=year).aggregate(models.Sum('amount'))

        return monthly_contribution

    def total_annual_contributions(self, year=current_year):
        annual_contribution = Contribution.objects.filter(
            year=year).aggregate(models.Sum('amount'))

        return annual_contribution

    def members_who_contributed(self, month, year=None):
        if year:
            summary = Contribution.objects.filter(
                month=month, year=year).values_list('member', flat=True)

        summary = Contribution.objects.filter(
                month=month).values_list('member', flat=True)

        return summary

    def available_funds(self):
        collected = self.total_contribution()
        disbursed = Disbursement.objects.aggregate(models.Sum('amount'))

        collected_ = collected.get('amount__sum')
        disbursed_ = disbursed.get('amount__sum')

        if not collected_ and disbursed_:
            available = 0 - disbursed_
        elif not disbursed_ and collected_:
            available = collected_ - 0
        elif not collected_ and not disbursed_:
            available = 0

        return {'disbursed_funds': disbursed_, 'available_funds': available}

    def __str__(self):
        return f'{self.month}: {self.amount}'


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
        return Disbursement.objects.aggregate(models.Sum('amount'))
