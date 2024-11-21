from django.urls import path
from .views import RegisterView,LoginView,getName
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/",LoginView.as_view(),name="login"),
    path("getName/",getName.as_view(),name="login")
    # path('login/', UserLoginView.as_view(), name='user_login'),
]
