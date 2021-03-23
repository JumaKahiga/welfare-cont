from rest_framework import generics

from members.models import Member
from members.serializers import (MemberSerializer, MembersSerializer)


class MembersListAPIView(generics.ListAPIView):
    # permissions = ()
    queryset = Member.objects.all()
    serializer_class = MembersSerializer


class MemberCreateAPIView(generics.CreateAPIView):
    # permissions = ()
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = "phone_number"
