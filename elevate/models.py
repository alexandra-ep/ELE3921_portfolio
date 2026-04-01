from django.db import models
from django.contrib.auth.models import User

#Instructor
class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to="instructors/", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

#ClassCategory
class ClassCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Class categories"
    
    def __str__(self):
        return self.name
    

#ClassType
class ClassType(models.Model):
    category = models.ForeignKey(ClassCategory, on_delete=models.CASCADE, related_name="class_types")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_capacity = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField()

    class Meta:
        unique_together = ('category', 'name')
    
    def __str__(self):
        return self.name
    

#LocationGroup
class LocationGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Location groups"

    def __str__(self):
        return self.name
    

#Location
class Location(models.Model):
    group = models.ForeignKey(LocationGroup, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    class Meta:
        unique_together = ('group', 'name')
    
    def __str__(self):
        return self.name


#FitnessClass
class FitnessClass(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE, related_name="fitness_classes")
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="fitness_classes")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="fitness_classes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    class Meta:
        verbose_name = "Fitness class"
        verbose_name_plural = "Fitness classes"

    def __str__(self):
        return f"{self.class_type.name} - {self.start_time.strftime('%d.%m.%Y %H:%M')}"
    
    def active_bookings_count(self):
        return self.bookings.filter(status='active').count()
    
    def spots_remaining(self):
        return self.capacity - self.active_bookings_count()
    
    def is_full(self):
        return self.spots_remaining() <= 0
    

#Bookings
class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'fitness_class'], name='unique_user_class_booking')
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.fitness_class}"