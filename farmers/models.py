from django.db import models

class Farmer(models.Model):
    farmer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    parish = models.CharField(max_length=100)
    land_location = models.CharField(max_length=150)
    land_size = models.DecimalField(max_digits=10, decimal_places=2)
    crop_type = models.CharField(max_length=100)

    def __str__(self):
        return self.farmer_name