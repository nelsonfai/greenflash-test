from django.db import models
from django.db.models.functions import TruncHour
from django.db.models import Sum
from django.db.models import Count

charging_speeds = (
    ( 2.3,"Level 1",),
    ( 9,"Level 2",),
    (60,"DC Fast Charging")
)

# Create your models here.
class ChargingStation(models.Model):
    name = models.CharField(max_length=100)
    stationid= models.CharField(max_length=100,unique=True,null=False,blank=False)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_functional = models.BooleanField(default=True,help_text='Verify if the station is functional')
    is_occupied = models.BooleanField(default=False,help_text='Verify if the station is Currently available for use')
    battery_capacity = models.DecimalField(max_digits=5, decimal_places=2,help_text='Current Battery level OF storage')
    charging_speed = models.DecimalField(max_digits=5, decimal_places=2,choices=charging_speeds,default=charging_speeds[2][1],help_text='level 1,level2 or fast charging')
    solar_panel_capacity = models.DecimalField(max_digits=6, decimal_places=2,help_text='Stations solar capacity.')
    solar_irradiance = models.DecimalField(max_digits=5, decimal_places=2,help_text='Solar intensity for a 16 day period using lon and lat values')
    solar_panel_efficiency = models.DecimalField(max_digits=4, decimal_places=2, help_text='Standard', default=22)
    usage_cost = models.FloatField(help_text='Cost per Kwh')
    def fast_charge_hours(self):
        charge_hours = (self.battery_capacity / self.charging_speed) / 1
        return charge_hours

    def __str__(self):
        return f'{self.name} - {self.stationid}' 
    
class ChargingSession(models.Model):
    user = models.CharField(default='Guest', max_length=50)
    charging_station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    energy_consumed = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def duration(self):
        return self.end_time - self.start_time
    def get_hourly_energy_consumption(target_date):
        charge_sessions = ChargingSession.objects.filter(start_time__date=target_date)
        charge_sessions = charge_sessions.annotate(hour=TruncHour('start_time'))
        charge_sessions = charge_sessions.values('hour').annotate(energy_consumed=Sum('energy_consumed'))
        hour_energy_dict = {session['hour']: session['energy_consumed'] for session in charge_sessions}
        return hour_energy_dict
    def get_hourly_session_counts(target_date):
            charge_sessions = ChargingSession.objects.filter(start_time__date=target_date)
            charge_sessions = charge_sessions.annotate(hour=TruncHour('start_time'))
            charge_sessions = charge_sessions.values('hour').annotate(count=Count('id'))
            hour_count_dict = {session['hour']: session['count'] for session in charge_sessions}
            return hour_count_dict
    def __str__(self):
        return f"{self.charging_station.name} - {self.user}"


"""
Level 1 Charging (Standard Household Outlet):

Energy Consumption Rate: Approximately 1.4 to 2.3 kilowatt-hours (kWh) per hour of charging.
Level 2 Charging (240-Volt AC Charging):

Energy Consumption Rate: Around 6 to 9 kWh per hour of charging, depending on the charging speed and efficiency.
DC Fast Charging:

Energy Consumption Rate: Typically ranges from 20 to 60 kWh per hour of charging, depending on the charging power and efficiency.
"""
