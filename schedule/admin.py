from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WeeklyAvailability

@admin.register(WeeklyAvailability)
class WeeklyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("professional", "weekday", "start_time", "end_time")
    list_filter = ("professional", "weekday")
