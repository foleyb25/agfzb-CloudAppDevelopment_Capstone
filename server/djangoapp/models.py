from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.description}"

class CarModel(models.Model):
    # CarType choices
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dealer_id = models.IntegerField()  # Referring to a dealer in Cloudant database
    car_type = models.CharField(max_length=50, choices=CAR_TYPE_CHOICES, default=SEDAN)
    year = models.DateField()  # You might want to use IntegerField if you just need the year

    def __str__(self):
        return f"{self.name} ({self.car_type}, {self.year.year})"



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
