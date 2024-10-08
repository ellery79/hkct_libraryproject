from django.db import models
from accounts.models import CustomUser
from books.models import Book
from datetime import date


# Create your models here.

class Borrow(models.Model):
    borrow_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    book_fine = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True, null=True)
    fine_paid = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(
        Book,  on_delete=models.DO_NOTHING, blank=True, null=True)
    overdue_days = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.book.title

    def is_overdue(self):
        return date.today() > self.due_date
