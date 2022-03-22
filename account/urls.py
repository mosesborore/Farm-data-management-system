from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("", views.redirect_to_login, name="home"),
    path("account/login/", views.login_view, name="login"),
    path("account/logout/", views.logout_view, name="logout"),
    path("account/signup/", views.signup, name="signup"),
    path("account/profile", views.profile, name="profile"),
]
