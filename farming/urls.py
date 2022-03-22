from django.urls import path

from . import views

app_name = "farming"

urlpatterns = [
    path("", views.farming_home_view, name="farming_home"),
]
