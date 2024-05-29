from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

# Create Customer Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username

# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate the profile thing
post_save.connect(create_profile, sender=User)


# Vehicles
# class Vehicle(models.Model):
#     make = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#     year = models.IntegerField()

#     def __str__(self):
#         return f"{self.make} {self.model} ({self.year})"

# Categories of Parts
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    

# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)


# All the Vehicle Parts
class Part(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    # compatible_vehicles = models.ManyToManyField(Vehicle, through='VehicleCompatibility')
    image = models.ImageField(upload_to='uploads/part/')

    # Add Sale Stuff
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return self.name
    

# Check if the part is compatible with the vehicle
# class VehicleCompatibilty(models.Model):
#     part = models.ForeignKey(Part, on_delete=models.CASCADE)
#     vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
#     notes = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.part.name} compatible with {self.vehicle}"



# Customer Orders
class Order(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.part
