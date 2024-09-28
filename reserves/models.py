from django.db import models
from accounts.models import CustomUser


# Create your models here.

reserve_choices = {
    'active': 'active',
    'fulfilled': 'fulfilled',
    'expired': 'expired',
} 

class Reserve(models.Model):
    reserve_date = models.DateField()
    reserve_status = models.CharField(choices=reserve_choices.items())
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)





def __str__(self):
    return self.title
