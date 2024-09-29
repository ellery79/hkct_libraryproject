from django.db import models

class Info(models.Model):
    info_email = models.EmailField(max_length=254)
    info_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.info_email
# Create your models here.
