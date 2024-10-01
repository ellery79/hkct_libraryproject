from django.contrib import admin
from borrows.models import Borrow


class BorrowAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'borrow_date', 'due_date', 'return_date')
    list_display_links = ('id', 'book', 'user')

# Register your models here
admin.site.register(Borrow, BorrowAdmin)
