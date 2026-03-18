from django.shortcuts import render
from .models import FitnessClass, Instructor


def home(request):
    return render(request, "home.html")


def classes_list(request):
    classes = FitnessClass.objects.all().order_by("start_time")
    return render(request, "classes_list.html", {"classes": classes})


def instructors_list(request):
    instructors = Instructor.objects.all().order_by("last_name")
    return render(request, "instructors_list.html", {"instructors": instructors})