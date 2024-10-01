from django.contrib import admin
from reserves.models import Reserve


class ReserveAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'reserve_date', 'reserve_status')
    list_display_links = ('id', 'book', 'user')

# Register your models here
admin.site.register(Reserve, ReserveAdmin)