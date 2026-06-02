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
    search_fields = ("first_name", "last_name", "email")

@admin.register(ClassCategory)
class ClassCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "default_capacity", "duration_minutes")
    list_filter = ("category",)
    search_fields = ("name", "category__name")

@admin.register(LocationGroup)
class LocationGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "group")
    list_filter = ("group",)
    search_fields = ("name", "group__name")

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = (
        "class_type",
        "instructor",
        "location",
        "start_time",
        "end_time",
        "capacity",
        "status",
        "spots_remaining",
        "is_full",
    )
    fields = ("class_type", "instructor", "location", "start_time", "end_time", "capacity", "status")
    readonly_fields = ("end_time",)

    list_filter = ("status", "location", "class_type", "instructor")
    search_fields = (
        "class_type__name",
        "instructor__first_name",
        "instructor__last_name",
        "location__name",
    )
    
    ordering = ("start_time",)
    date_hierarchy = "start_time"
    list_select_related = ("class_type", "instructor", "location")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "fitness_class", "status", "created_at")
    list_filter = ("status", "fitness_class")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "fitness_class__class_type__name",
    )
    ordering = ("-created_at",)
    list_select_related = ("user", "fitness_class")

