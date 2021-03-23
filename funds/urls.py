from django.urls import path

from funds.views import (
    TotalContributionsAPIView)

app_name = 'funds'

urlpatterns = [
    path('summary', TotalContributionsAPIView.as_view())
]
