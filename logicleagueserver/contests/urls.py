from django.urls import path
from . import views

urlpatterns = [
    # Public contest list
    path('', views.contest_list, name='contest-list'),
    
    # Contest registration
    path('contests/<int:contest_id>/register/', views.contest_registration, name='contest-registration'),

    # Admin view: list all contests and create a new contest
    path('admin/contests/', views.contest_admin_list, name='contest-admin-list'),
    
    # Admin view: specific contest details, update, or delete
    path('admin/contests/<int:contest_id>/', views.contest_admin_detail, name='contest-admin-detail'),  # DELETE is handled here

    # Add a problem to a contest
    path('admin/contests/<int:contest_id>/addchallenge/', views.add_challenges_to_contest, name='add-problem-to-contest'),

    # Contest detail view for non-admin users (can view details)
    path('contests/<int:contest_id>/', views.contest_detail, name='contest-detail'),
    
    # Admin manage view (if needed)
    path('admin/manage/', views.contest_admin_manage, name='contest-admin-manage'),

    # Admin-specific endpoint to delete a contest explicitly (optional but adds clarity)
    path('admin/contests/<int:contest_id>/delete/', views.delete_contest, name='delete-contest'),
  # Same as contest_admin_detail (DELETE)
]
