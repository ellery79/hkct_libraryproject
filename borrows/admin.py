from django.contrib import admin
from borrows.models import Borrow


class BorrowAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'borrow_date', 'due_date',
                    'return_date', 'overdue_days', 'book_fine', 'fine_paid')
    list_display_links = ('id', 'book', 'user')
    list_editable = ('fine_paid',)
    list_filter = ('user',)


# Register your models here
admin.site.register(Borrow, BorrowAdmin)
