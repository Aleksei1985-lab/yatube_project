from django.contrib import admin

# Register your models here.
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_at', 'author', 'location')
    search_fields = ('name', 'description')
    list_filter = ('start_at', 'author')