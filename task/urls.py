from django.urls import path 
from . import views


app_name = 'task'

urlpatterns = [
	path("", views.task_home_view, name="task_home"),
]
