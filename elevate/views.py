from django.shortcuts import render
from .models import FitnessClass


def home(request):
    return render(request, "home.html")


def classes_list(request):
    classes = FitnessClass.objects.all().order_by("start_time")
    return render(request, "classes_list.html", {"classes": classes})