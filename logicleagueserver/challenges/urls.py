from django.urls import path,include
from .views import ChallengeCreateView , SolutionHandel

urlpatterns = [
    path("challenges/",ChallengeCreateView.as_view(),name="challenge"),
    path("solution/",SolutionHandel.as_view())
]
