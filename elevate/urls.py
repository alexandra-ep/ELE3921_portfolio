from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("classes/", views.classes_list, name="classes_list"),
]