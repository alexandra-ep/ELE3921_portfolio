from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("classes/", views.classes_list, name="classes_list"),
    path("classes/<int:class_id>/", views.class_detail, name="class_detail"),
    path("classes/<int:class_id>/book/", views.book_class, name="book_class"),
    path("bookings/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("instructors/", views.instructors_list, name="instructors_list"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("profile/change-password/", views.change_password, name="change_password"),
    path("accounts/register/", views.register, name="register"),
]