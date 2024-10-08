from django.db import models
from libraries.choices import district_choices

class Library(models.Model):
    district = models.CharField(max_length=200, 
                                choices=[(key, value) for key, value in district_choices.items()]
                                )
    address = models.CharField(max_length=200)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    map_url = models.CharField(max_length=255)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()

    def __str__(self):
        return self.district