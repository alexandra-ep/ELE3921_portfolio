from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("classes/", views.classes_list, name="classes_list"),
    path("classes/<int:class_id>/", views.class_detail, name="class_detail"),
    path("instructors/", views.instructors_list, name="instructors_list"),
    path("accounts/register/", views.register, name="register"),
]