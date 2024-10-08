from django.db import models
from datetime import datetime
from libraries.models import Library

status_choices = {
    'Borrowed': 'Borrowed',
    'Reserved': 'Reserved',
    'Available': 'Available',
    'Lost': 'Lost',
}
# Create your models here.


class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    copy = models.IntegerField(blank=True, null=True)
    publication_year = models.CharField(max_length=200, blank=True, null=True)
    publisher = models.CharField(max_length=200)
    call_number = models.CharField(max_length=200)
    edition = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=200)
    barcode = models.CharField(max_length=50)
    book_status = models.CharField(
        max_length=50, choices=status_choices.items())
    is_latest = models.BooleanField(default=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    photo_main = models.ImageField(
        upload_to='photos/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.copy}"
