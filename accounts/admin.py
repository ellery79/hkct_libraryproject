from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Rule

# Register your models here.
# Add fields to admin panel
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
           (None, {'fields': ('rule', 'card_id', 'user_phone')}),
       )

admin.site.register(CustomUser, CustomUserAdmin)

# Add Rule to admin site panel
admin.site.register(Rule)
