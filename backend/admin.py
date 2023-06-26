from django.contrib import admin

# Register your models here
from .models import ChargingSession,ChargingStation

admin.site.register(ChargingStation)
admin.site.register(ChargingSession)