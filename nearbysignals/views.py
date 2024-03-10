from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from app.models import DriverAppSignal
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of Earth in kilometers

    return distance

def find_nearby_points(target_lat, target_lon, max_distance=100):
    signals = DriverAppSignal.objects.all()
    nearby_points = []
    for signal in signals:
        distance = haversine(target_lat, target_lon, signal.latitude, signal.longitude)
        if distance <= max_distance:
            nearby_points.append({
                'latitude': signal.latitude,
                'longitude': signal.longitude,
                'timestamp': signal.timestamp
            })
    return nearby_points

def nearby_points_view(request, target_lat, target_lon):
    nearby_points = find_nearby_points(float(target_lat), float(target_lon))
    return JsonResponse({'nearby_points': nearby_points})
