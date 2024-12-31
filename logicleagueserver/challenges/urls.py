from django.urls import path,include
from .views import ChallengeCreateView , SolutionHandle,Challenge,testCaseView,get_test_case_view

urlpatterns = [
    # get admin challenge route
    path("challenge/admin",ChallengeCreateView.as_view(),name="challenge"),
    #display challenge rot
    path("challenge/",Challenge.as_view() ),
    # get challenge by id route
    path("challenge/<slug:challengeID>/", Challenge.as_view(),name="getchallenge" ),
    # get all testcases for a given challenge id
    path("challenge/<slug:challengeID>/testCase/",get_test_case_view),
    # get tescases view [testcaseid,marks,smaple] for a given challegne id
    path("challenge/admin/<slug:challengeID>/testCase/",testCaseView.as_view()),
    # get testcases data for admin o a given challenge particular test case
    path("challenge/admin/<slug:challengeID>/<int:edit>/testCase/<slug:testCaseID>/",testCaseView.as_view()),
    
    path("solution/",SolutionHandle.as_view())
    
]
