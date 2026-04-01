from django.contrib import admin
from .models import (
    Instructor,
    ClassCategory,
    ClassType,
    LocationGroup,
    Location,
    FitnessClass,
    Booking
)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")

@admin.register(ClassCategory)
class ClassCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "default_capacity", "duration_minutes")
    list_filter = ("category",)

@admin.register(LocationGroup)
class LocationGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "group")
    list_filter = ("group",)

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ("class_type", "instructor", "location", "start_time", "capacity", "status")
    list_filter = ("status", "location", "class_type")
    search_fields = ("class_type__name", "instructor__first_name", "instructor__last_name")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "fitness_class", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username",)

