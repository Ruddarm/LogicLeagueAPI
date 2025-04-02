from django.urls import path
from . import views

urlpatterns = [
    # Public contest list
    # path('', views.contest_list, name='contest-list'),
    path('', views.ContestCreationView.as_view(), name='contestcreation'),
    path('edit/<uuid:contest_id>/', views.ContestCreationView.as_view(), name='contest-edit'),  # ✅ FIXED
    path('<uuid:contest_id>/', views.ContestCreationView.as_view()),  # ✅ FIXED
    path('<uuid:contest_id>/challenges/', views.ContestChallengeManageView.as_view(), name='contest-challenge-manage'),
    path("list/", views.ContestListview.as_view(), name="contest-list"),
    path('<uuid:contest_id>/challenges/<uuid:challenge_id>/remove/', views.ContestChallengeManageView.as_view(), name='contest-challenge-remove'),

    # Contest registration
    # path('contests/<int:contest_id>/register/', views.contest_registration, name='contest-registration'),

    # # Admin view: list all contests and create a new contest
    # path('admin/contests/', views.contest_admin_list, name='contest-admin-list'),
    
    # # Admin view: specific contest details, update, or delete
    # path('admin/contests/<int:contest_id>/', views.contest_admin_detail, name='contest-admin-detail'),

    # # Contest detail view for non-admin users (can view details)
    # path('contests/<int:contest_id>/', views.contest_detail, name='contest-detail'),
    # path('admin/manage/', views.contest_admin_list, name='contest-admin-manage'),
]
