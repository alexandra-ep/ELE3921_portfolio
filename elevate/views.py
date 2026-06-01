from django.shortcuts import render, get_object_or_404, redirect
from .forms import RegisterForm, BookingForm, CancelBookingForm, ProfileUpdateForm
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import FitnessClass, Instructor, Booking, ClassCategory, Location


def home(request):
    upcoming_classes = FitnessClass.objects.filter(
        start_time__gte=timezone.now(),
        status="scheduled"
    ).order_by('start_time')[:3]

    return render(request, 'home.html', {
        'upcoming_classes': upcoming_classes
    })


def classes_list(request):
    classes = FitnessClass.objects.filter(
        start_time__gte=timezone.now(),
        status="scheduled"
    ).order_by("start_time")

    categories = ClassCategory.objects.all().order_by("name")
    locations = Location.objects.all().order_by("name")

    selected_category = request.GET.get("category")
    selected_location = request.GET.get("location")
    selected_date = request.GET.get("date")

    if selected_category:
        classes = classes.filter(class_type__category_id=selected_category)
    
    if selected_location:
        classes = classes.filter(location_id=selected_location)

    if selected_date:
        classes = classes.filter(start_time__date=selected_date)

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
        "selected_date": selected_date,
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
            fitness_class=fitness_class,
            status="active"
        ).first()
    
    return render(request, "class_detail.html", {
        "fitness_class": fitness_class,
        "user_booking": user_booking
    })


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(
                request, 
                "Your account has been created successfully. You are now logged in.",
                extra_tags="registration-popup"
            )

            return redirect("home")
    else:
        form = RegisterForm()
    
    return render (request, "registration/register.html", {"form": form})


 
@login_required
@require_POST
def book_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    form = BookingForm(request.POST)

    # Check if user already booked this class
    existing_booking = Booking.objects.filter(
        user=request.user,
        fitness_class=fitness_class,
        status="active"
    ).exists()

    if not form.is_valid():
        messages.warning(request, "Invalid booking request.")

    elif fitness_class.start_time <= timezone.now():
        messages.warning(request, "You cannot book a class that has already started or passed.")
    
    elif fitness_class.status != "scheduled":
        messages.warning(request, "This class is not available for booking.")
    
    elif existing_booking:
        messages.warning(request, "You have already booked this class.")

    elif fitness_class.is_full():
        messages.warning(request, "Sorry, this class is fully booked.")

    else:
        Booking.objects.create(
            user=request.user,
            fitness_class=fitness_class,
            status="active"
        )
        messages.success(request, "Your class has been booked successfully.")
    
    next_page = request.POST.get("next")

    if next_page == "class_detail":
        return redirect("class_detail", class_id=fitness_class.id)

    return redirect("classes_list")


@login_required
@require_POST
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status="active"
    )

    fitness_class = booking.fitness_class
    next_page = request.POST.get("next")
    form = CancelBookingForm(request.POST)

    if not form.is_valid():
        messages.warning(request, "Invalid cancellation request.")

    elif fitness_class.can_cancel():
        booking.status = "cancelled"
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
        
    else:
        messages.warning(request, "You cannot cancel this booking within 3 hours of the class start time.")

    if next_page == "my_bookings":
        return redirect("my_bookings")
    
    if next_page == "class_detail":
        return redirect("class_detail", class_id=fitness_class.id)

    return redirect("class_detail", class_id=fitness_class.id)


@login_required
def my_bookings(request):
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        status="active",
        fitness_class__start_time__gte=timezone.now()
    ).select_related(
        "fitness_class",
        "fitness_class__class_type",
        "fitness_class__instructor",
        "fitness_class__location"
    ).order_by("fitness_class__start_time")

    past_bookings = Booking.objects.filter(
        user=request.user,
        status="active",
        fitness_class__start_time__lt=timezone.now()
    ).select_related(
        "fitness_class",
        "fitness_class__class_type",
        "fitness_class__instructor",
        "fitness_class__location"
    ).order_by("-fitness_class__start_time")

    cancelled_bookings = Booking.objects.filter(
        user=request.user,
        status="cancelled"
    ).select_related(
        "fitness_class",
        "fitness_class__class_type",
        "fitness_class__instructor",
        "fitness_class__location"
    ).order_by("-fitness_class__start_time")

    profile_form = ProfileUpdateForm(instance=request.user)

    return render(request, "my_bookings.html", {
        "bookings": upcoming_bookings,
        "upcoming_bookings": upcoming_bookings,
        "past_bookings": past_bookings,
        "cancelled_bookings": cancelled_bookings,
        "profile_form": profile_form,
    })

@login_required
@require_POST
def update_profile(request):
    form = ProfileUpdateForm(request.POST, instance=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Your personal information has been updated")
    else:
        messages.warning(request, "Your personal information could not be updated. Please check the form.")
    
    return redirect("my_bookings")