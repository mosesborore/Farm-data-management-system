from django.urls import path

from . import views

app_name = 'farm'

urlpatterns = [
	path("", views.farm_home_view, name='farm-home'),
	path('soil', views.soil_detail, name="soil-detail"),
	path('farm/edit/<int:pk>', views.edit_farm, name="edit-farm-detail"),
	path("farm/delete/<int:pk>", views.delete_farm, name="delete-farm-detail"),
	path("soil/edit/<int:pk>", views.edit_soil_detail, name="edit-soil-detail"),
	path("soil/delete/<int:pk>", views.delete_soil, name="delete-soil-detail"),

]
