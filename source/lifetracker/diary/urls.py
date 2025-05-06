from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [
    path("", views.diary_list, name="list"),
    path("create/", views.diary_create, name="create"),
    path("<int:pk>/update/", views.diary_update, name="update"),
    path("<int:pk>/delete/", views.diary_delete, name="delete"),
] 