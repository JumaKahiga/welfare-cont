from django.urls import path

from members.views import (
    MembersListAPIView, MemberCreateAPIView, MemberUpdateAPIView)

app_name = 'members'

urlpatterns = [
    path('', MembersListAPIView.as_view()),
    path('new_member', MemberCreateAPIView.as_view()),
    path('member/<phone_number>/update', MemberUpdateAPIView.as_view())
]
