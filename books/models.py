from django.db import models
from libraries.models import Library, district_choices
from books.choices import status_choices

class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    copy = models.IntegerField(blank=True, null=True)
    publication_year = models.CharField(max_length=200, blank=True, null=True)
    publisher = models.CharField(max_length=200)
    call_number = models.CharField(max_length=200)
    edition = models.CharField(max_length=200, blank=True, null=True)
    isbn = models.CharField(max_length=200)
    barcode = models.CharField(max_length=50)
    book_status = models.CharField(max_length=50, 
                                   choices=[(key, value) for key, value in status_choices.items()]
                                   )
    is_latest = models.BooleanField(default=True)
    description = models.TextField(max_length=200, blank=True, null=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.title
    
# class BookLibrary(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     library = models.ForeignKey(Library, on_delete=models.CASCADE)
    
#     class Meta:
#         unique_together = ('book', 'library')  # Prevents duplicate entries
