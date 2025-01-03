from django.urls import path
from . import views

urlpatterns = [
    # User endpoints
    path('', views.contest_list, name='contest-list'),  # List and create contests
    path('<int:contest_id>/', views.contest_detail, name='contest-detail'),  # Contest details
    path('<int:contest_id>/registration/', views.contest_registration, name='contest-registration'),
  # Registration

    # Admin endpoints
    path('admin/', views.contest_admin_list, name='contest-admin-list'),  # Admin list and create contests
    path('admin/<int:contest_id>/', views.contest_admin_detail, name='contest-admin-detail'),  # Admin contest management
]
