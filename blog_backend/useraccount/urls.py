from django.urls import path

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

from . import api

urlpatterns = [
    path('register/', RegisterView.as_view(), name='rest_register'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    path('<uuid:pk>/', api.author_detail, name='api_user_detail'),
    path('profile/<str:pk>/', api.profile_detail, name='profile_detail'),
    path('users/', api.users_list, name='users_list'),
    path('manager/<str:pk>/', api.manager_detail, name='manager_detail'),
]