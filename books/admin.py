from django.contrib import admin

# Register your models here.
from books.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'copy','book_status',  'publication_year', 'publisher',
                    'call_number', 'edition', 'isbn', 'barcode', 'is_latest', 'library')
    list_display_links = ('id', 'title')
    list_filter = ('library', 'book_status',)
    list_editable = ('is_latest', 'book_status')
    search_fields = ('title', 'author', 'copy', 'barcode', 'isbn', 'library')
    list_per_page = 25


admin.site.register(Book, BookAdmin)
