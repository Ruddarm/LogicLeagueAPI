from django.urls import path,include
from .views import ChallengeCreateView , SolutionHandle,Challenge,testCaseView

urlpatterns = [
    path("challenge/",ChallengeCreateView.as_view(),name="challenge"),
    path("challenge/<str:challengeID>/", Challenge.as_view(),name="getchallenge" ),
    path("challenge/<str:challengeID>/testCase/",testCaseView.as_view()),
    path("solution/",SolutionHandle.as_view())
    
]
