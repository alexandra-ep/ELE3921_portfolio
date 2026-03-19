from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import FitnessClass, Instructor, Booking


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

    user_booking = None

    if request.user.is_authenticated:
        user_booking = Booking.objects.filter(
            user=request.user,
            fitness_class=fitness_class
        ).first()
    
    return render(request, "class_detail.html", {
        "fitness_class": fitness_class,
        "user_booking": user_booking
    })


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


 
@login_required
def book_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)

    # Check if user already booked this class
    existing_booking = Booking.objects.filter(
        user=request.user,
        fitness_class=fitness_class
    ).exists()
    
    if not existing_booking and not fitness_class.is_full():
        Booking.objects.create(
            user=request.user,
            fitness_class=fitness_class
        )

    return redirect("class_detail", class_id=fitness_class.id)


@login_required
def cancel_booking(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)

    booking = Booking.objects.filter(
        user=request.user,
        fitness_class=fitness_class
    ).first()

    if booking:
        booking.delete()

    return redirect("class_detail", class_id=fitness_class.id)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        "fitness_class",
        "fitness_class__class_type",
        "fitness_class__instructor",
        "fitness_class__location"
    ).order_by("fitness_class__start_time")

    return render(request, "my_bookings.html", {"bookings": bookings})