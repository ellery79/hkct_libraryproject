from django.db import models

# Create your models here.

class borrows(models.Model):
    reserve_date = models.DateTimeField()

    reserve_status = models.CharField (choices=reserve_choices.items())


def __str__(self):
        return self.title   
    

