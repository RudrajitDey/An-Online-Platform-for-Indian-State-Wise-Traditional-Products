from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.user_profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="profile_edit"),
    path("profile/password/", views.change_password, name="profile_password"),

    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),

    path("activate/<uidb64>/<token>/", views.activate, name='activate'),

    path("forgotPassword/", views.forgotPassword, name="forgotPassword"),
    path("resetpassword_validate/<uidb64>/<token>/", views.resetpassword_validate, name='resetpassword_validate'),
    path("resetPassword/", views.resetPassword, name="resetPassword"),


]