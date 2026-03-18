from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import FitnessClass, Instructor


def home(request):
    return render(request, "home.html")


def classes_list(request):
    classes = FitnessClass.objects.all().order_by("start_time")
    return render(request, "classes_list.html", {"classes": classes})


def instructors_list(request):
    instructors = Instructor.objects.all().order_by("last_name")
    return render(request, "instructors_list.html", {"instructors": instructors})


def class_detail(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    return render(request, "class_detail.html", {"fitness_class": fitness_class})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            login(request, user)

            return redirect("home")
    else:
        form = UserCreationForm()
    
    return render (request, "registration/register.html", {"form": form})