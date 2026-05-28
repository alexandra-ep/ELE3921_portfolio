from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FitnessClass, Instructor, Booking, ClassCategory, Location


def home(request):
    upcoming_classes = FitnessClass.objects.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time')[:3]

    return render(request, 'home.html', {
        'upcoming_classes': upcoming_classes
    })


def classes_list(request):
    classes = FitnessClass.objects.all().order_by("start_time")

    categories = ClassCategory.objects.all().order_by("name")
    locations = Location.objects.all().order_by("name")

    selected_category = request.GET.get("category")
    selected_location = request.GET.get("location")

    if selected_category:
        classes = classes.filter(class_type__category_id=selected_category)
    
    if selected_location:
        classes = classes.filter(location_id=selected_location)

    booked_class_ids = []

    if request.user.is_authenticated:
        booked_class_ids = Booking.objects.filter(
            user=request.user,
            status="active"
        ).values_list("fitness_class_id", flat=True)

    return render(request, "classes_list.html", {
        "classes": classes,
        "booked_class_ids": booked_class_ids,
        "categories": categories,
        "locations": locations,
        "selected_category": selected_category,
        "selected_location": selected_location,
})

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
        email = request.POST.get("email")

        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
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

    if existing_booking:
        messages.warning(request, "You have already booked this class.")

    elif fitness_class.is_full():
        messages.warning(request, "Sorry, this class is full.")

    else:
        Booking.objects.create(
            user=request.user,
            fitness_class=fitness_class
        )
        messages.success(request, "Your class has been booked successfully.")
    
    next_page = request.POST.get("next")

    if next_page == "class_detail":
        return redirect("class_detail", class_id=fitness_class.id)

    return redirect("classes_list")


@login_required
def cancel_booking(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)

    booking = Booking.objects.filter(
        user=request.user,
        fitness_class=fitness_class
    ).first()

    next_page = request.POST.get("next")

    if booking:
        if fitness_class.can_cancel():
            booking.delete()
            messages.success(request, "Your booking has been cancelled.")
        else:
            messages.warning(request, "You cannot cancel this booking within 3 hours of the class start time.")
    else:
        messages.warning(request, "No booking was found for this class.")

    if next_page == "my_bookings":
        return redirect("my_bookings")
    
    if next_page == "class_detail":
        return redirect("class_detail", class_id=fitness_class.id)

    return redirect("class_detail", class_id=fitness_class.id)


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user,
        fitness_class__start_time__gte=timezone.now()
    ).select_related(
        "fitness_class",
        "fitness_class__class_type",
        "fitness_class__instructor",
        "fitness_class__location"
    ).order_by("fitness_class__start_time")

    return render(request, "my_bookings.html", {"bookings": bookings})
