from django.urls import path
from .views import LandingPageView, UserRegisterView, UsersLogoutView, UsersLoginView, ProfileView, SettingsProfileView

urlpatterns = [
    path('', LandingPageView.as_view(), name='landing'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UsersLoginView.as_view(), name='login'),
    path('logout/', UsersLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('settings/', SettingsProfileView.as_view(), name='settings')
]