from django.db import models

# Create your models here.

class  Borrow(models.Model):
    borrow_date = models.DateTimeField()
    due_date = models.DateTimeField()
    return_date = models.DateTimeField()
    book_fine = models.DecimalField()
    fine_paid = models.BooleanField()


    

    def __str__(self):
        return self.name
