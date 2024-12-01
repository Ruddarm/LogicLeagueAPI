from django.urls import path,include
from .views import ChallengeCreateView

urlpatterns = [
    path("challenge/",ChallengeCreateView.as_view(),name="challenge")
]
