from django.contrib import admin
from books.models import Book, Library

class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'copy', 'publication_year', 'publisher', 
        'call_number', 'edition', 'isbn', 'barcode', 'book_status', 
        'is_latest', 'description', 'library'
    )
    list_display_links = ('id', 'title')
    list_editable = ('is_latest',)
    search_fields = ('title', 'author', 'copy', 'barcode', 'isbn')
    list_per_page = 25
        
# Register the Book model
admin.site.register(Book, BookAdmin)