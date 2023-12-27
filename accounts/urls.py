from django.urls import path
from .views import UserSignupView, UserSignInView, UserLogoutView, UserProfileView

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("signin/", UserSignInView.as_view(), name="signin"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
