from django.urls import path,include
from .views import ChallengeCreateView , SolutionHandel

urlpatterns = [
    path("challenge/",ChallengeCreateView.as_view(),name="challenge"),
    path("challenge/post",SolutionHandel.as_view())
]
