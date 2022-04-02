from django.urls import path

from . import views

app_name = "task"

urlpatterns = [
    path("", views.task_home_view, name="home"),
    path("add/", views.add_task, name="add-task"),
    path("status=<str:status>", views.filter_task, name="filter-task"),
    path("<int:pk>/delete", views.delete_task, name="delete-task"),
    path("<int:pk>/task", views.edit_task, name="edit-task"),
]
