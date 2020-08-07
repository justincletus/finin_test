from django.contrib import admin
from .models import Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'dob',
        'email_confirmed',
        'token',
        'mobile',
    ]

    list_filter = [
        'user',
        'email_confirmed',
        'mobile'
    ]
