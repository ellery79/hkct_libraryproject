from django.db import models
from datetime import datetime

district_choices = {
    'Central': 'Central Library',
    'Kowloon': 'Kowloon Library', 
    'New Territories': 'New Territories Library',
    }
# Create your models here.
class Library(models.Model):
    district = models.CharField(max_length=200, choices=district_choices.items())
    address = models.CharField(max_length=200)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    map_url = models.CharField(max_length=50)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()

def __str__(self):
    return self.name