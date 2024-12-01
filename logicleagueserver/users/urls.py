from django.urls import path,include
from .views import RegisterView,LoginView,getName,GoogleLogin,LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("login/",LoginView.as_view(),name="login"),
    path("getName/",getName.as_view(),name="login"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path('api/auth/', include('dj_rest_auth.urls')),
    # path('api/auth/google/', include('social_django.urls', namespace='social')),
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),

    # path('login/', UserLoginView.as_view(), name='user_login'),
]
