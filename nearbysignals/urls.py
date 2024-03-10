from django.urls import path

from nearbysignals.views import nearby_points_view

urlpatterns = [
    path('nearby_points/<str:target_lat>/<str:target_lon>/', nearby_points_view, name='nearby_points_view'),
]
