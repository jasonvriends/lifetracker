from django.urls import path
from . import views

app_name = "diary"

urlpatterns = [
    path("", view=views.diary_list, name="list"),
    path("create/", view=views.diary_create, name="create"),
    path("<int:pk>/update/", view=views.diary_update, name="update"),
    path("<int:pk>/delete/", view=views.diary_delete, name="delete"),
    path("favorites/", view=views.favorites, name="favorites"),
] 