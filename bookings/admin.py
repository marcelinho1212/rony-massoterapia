from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "professional", "service", "start", "status")
    list_filter = ("professional", "status")
    search_fields = ("customer_name", "customer_whatsapp")
