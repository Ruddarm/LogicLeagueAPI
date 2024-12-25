from django.urls import path,include
from .views import ChallengeCreateView , SolutionHandle

urlpatterns = [
    path("challenges/",ChallengeCreateView.as_view(),name="challenge"),
    path("solution/",SolutionHandle.as_view())
]
