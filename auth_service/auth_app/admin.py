from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'verified', 'password')
    search_fields = ('email', 'verified')


admin.site.register(User, UserAdmin)
