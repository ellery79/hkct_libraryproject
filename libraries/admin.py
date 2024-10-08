from django.contrib import admin
from libraries.models import Library

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'district', 'address', 'phone', 'email', 'map_url', 'opening_hour', 'closing_hour',)
    list_display_links = ('id', 'district',)
    search_fields = ('district',)
    list_per_page = 10

# Register the Library model
admin.site.register(Library, LibraryAdmin)