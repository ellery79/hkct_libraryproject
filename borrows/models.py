from django.db import models

from accounts.models import CustomUser


# Create your models here.

class Borrow(models.Model):
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField()
    book_fine = models.DecimalField(decimal_places=2, max_digits=3)
    fine_paid = models.BooleanField()
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name
