from django.shortcuts import render
import json
import os
from django.db.models import Sum
from .models import ChargingStation,ChargingSession
from datetime import datetime
from django_pandas.io import read_frame
from datetime import timedelta

# Create your views here.
def home(request):
    charging_stations = ChargingStation.objects.all()
    station_count = charging_stations.count()
    functional = charging_stations.filter(is_functional=True).count()
    out_of_order = station_count - functional
    available = charging_stations.filter(is_occupied=False).count()

    defect_stations = charging_stations.filter(is_functional=False)
    messages = write_messages(defect_stations)

    total_energy_consumed = ChargingSession.objects.aggregate(total_energy=Sum('energy_consumed')).get('total_energy')
    session_count = ChargingSession.objects.count()
    target_date = datetime(2023, 6, 13).date()

    hourly_energy_consumption = ChargingSession.get_hourly_energy_consumption(target_date)
    hour_labels_energy =[hour.strftime('%H') for hour in hourly_energy_consumption.keys()]# list(hourly_energy_consumption.keys())
    energy_values =[float(value) for value in hourly_energy_consumption.values()] # list(hourly_energy_consumption.values())

    hourly_session_counts = ChargingSession.get_hourly_session_counts(target_date)
    hour_labels = [hour.strftime('%H') for hour in hourly_session_counts.keys()] #list(hourly_session_counts.keys()) 
    count_values = list(hourly_session_counts.values())

    context = {
        'station_count': station_count,
        'functional': functional,
        'out_of_order': out_of_order,
        'available': available,
        'messages': messages,
        'total_energy_consumed': round(total_energy_consumed, 3),
        'session_count': session_count,
        'hour_labels': hour_labels,
        'count_values': count_values,
        'energy_values': energy_values,
        'hour_labels_energy': hour_labels_energy
    }

    return render(request, 'backend/index.html', context=context)


def addto ():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
                name = item['AddressInfo']['Title']
                stationid =item['ID']
                location = item['AddressInfo']['AddressLine1']
                latitude = item['AddressInfo']['Latitude']
                longitude = item['AddressInfo']['Longitude']
                battery_capacity = 40
                solar_panel_capacity = item['Connections'][0]['PowerKW']
                usage_cost = 0.34
                solar_irradiance= 0
        # Create the ChargingStation object
                charging_station = ChargingStation(
                    name=name,
                    stationid=stationid,
                    location=location,
                    latitude=latitude,
                    longitude=longitude,
                    battery_capacity=battery_capacity,
                    solar_panel_capacity=solar_panel_capacity,
                    usage_cost=usage_cost,
                    solar_irradiance=solar_irradiance
                )
                charging_station.save()
                print(f'{name} DONE')

def stations(request):
    stations = ChargingStation.objects.all()
    context={
         'stations':stations
    }
    return render (request, 'backend/stations.html', context=context)

def station_overview(request,id):
    target_date = datetime(2023, 6, 13).date()
    station = ChargingStation.objects.get(stationid=id)
    sessions = ChargingSession.objects.filter(charging_station=station)
    session_count = sessions.count()
    total_energy= sessions.aggregate(total_energy=Sum('energy_consumed')).get('total_energy')
    total_duration = timedelta()

    if total_energy:
        total_energy_consumed =f'{round(total_energy,3)}kW'
       
    else:
        total_energy_consumed = 0
        print('got here')


    for session in sessions:
            total_duration += session.duration

    if session_count == 0:
        average_duration = 0
    else:
        average_duration = total_duration/session_count

    context = {
         'station': station,
         'session_count':session_count,
         'total_energy_consumed':total_energy_consumed,
         'average_duration':average_duration
     }
    return render (request,'backend/station.html',context=context)

def write_messages(data):
    messages = []
    for item in data:
        message = f'Defect at {item.name}-{item.stationid} Station'
        messages.append(message) 

    return messages

