from rest_framework import generics

from funds.models import Contribution
from funds.serializers import (
    FundsSerializer, ContributionSerializer)


class TotalContributionsAPIView(generics.ListAPIView):
    # permissions = ()
    serializer_class = FundsSerializer
    queryset = Contribution.objects.filter(id=1)


class ContributeAPIView(generics.CreateAPIView):
    # permissions = ()
    serializer_class = ContributionSerializer
    queryset = Contribution.objects.all()
