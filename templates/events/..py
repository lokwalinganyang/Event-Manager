from django.contrib import admin
from .models import Event, Registration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'max_participants', 'registered_count', 'is_full']
    list_filter = ['date', 'location']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'event', 'registered_at']
    list_filter = ['event', 'registered_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['registered_at']