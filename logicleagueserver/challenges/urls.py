from django.urls import path,include
from .views import challenge_admin_view , SolutionHandle,challenge_user_view,testcase_admin_view,get_test_case_view_terminal,get_test_case_view_desc

urlpatterns = [
    # create challenge by admin
    path("challenge/admin",challenge_admin_view.as_view(),name="challenge"),
    # update/delete challenge by admin
    path("challenge/admin/<slug:challengeID>/",challenge_admin_view.as_view(),name="challenge"),
    # get challenge by challenge data for admin
    path("challenge/admin/<slug:challengeID>/testCase/",testcase_admin_view.as_view()),
    #to pefrom delete and update of a testcase
    path("challenge/admin/<slug:challengeID>/testCase/<slug:testCaseID>/",testcase_admin_view.as_view()),
    # get testcases data for admin o a given challenge particular test case
    path("challenge/admin/<slug:challengeID>/<int:edit>/testCase/<slug:testCaseID>/",testcase_admin_view.as_view()),
    #display challenge for  user
    path("challenge/",challenge_user_view.as_view() ),
    # get challenge by challenge id for user
    path("challenge/<slug:challengeID>/", challenge_user_view.as_view(),name="getchallenge" ),
    # get all testcases for a given challenge id for terminal view withtou explaination
    path("challenge/<slug:challengeID>/testCase/",get_test_case_view_terminal),
    # get all testcases for a given challenge id for description with explantion
    path("challenge/<slug:challengeID>/testCase/desc",get_test_case_view_desc),
    # get tescases view [testcaseid,marks,smaple] for a given challegne id
    path("challenge/runcode/<slug:challengeID>/",SolutionHandle.as_view())
    
]
