from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# from app.models import Book
# from .serializer import TeacherSerializer, BookSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .tasks import process_signal
import firebase_admin
from app.middleware import FirebaseInitMiddleware
from firebase_admin import auth
from .models import Journey
from django.core import serializers
from django.shortcuts import get_object_or_404
from app.models import Journey, DriverJourney, Driver, Route, HealthcareFacility


def get_journey_by_driver_id(request, driver_id):
    try:
        # Check if the driver_id is in the DriverJourney table and active is True
        driver_journey = DriverJourney.objects.get(driver_id=driver_id, active=True)
        journey = Journey.objects.get(id=driver_journey.journey_id)

        # Get the full driver object
        driver = Driver.objects.get(id=driver_journey.driver_id)

        # Get the full route object
        route = Route.objects.get(id=journey.route_id)

        # Get the full facility objects for start_facility and end_facility
        start_facility = HealthcareFacility.objects.get(id=route.start_facility_id)
        end_facility = HealthcareFacility.objects.get(id=route.end_facility_id)

        data = {
            'id': journey.id,
            'status': journey.status,
            'driver_id': journey.driver_id,
            'patient_case_id': journey.patient_case_id,
            'route_id': journey.route_id,
            'driver': {
                'id': driver.id,
                'first_name': driver.first_name,
                'last_name': driver.last_name,
                'license_number': driver.license_number
            },
            'route': {
                'id': route.id,
                'start_facility': {
                    'id': start_facility.id,
                    'name': start_facility.name,
                    'location_lat': start_facility.location_lat,
                    'location_lon': start_facility.location_lon
                },
                'end_facility': {
                    'id': end_facility.id,
                    'name': end_facility.name,
                    'location_lat': end_facility.location_lat,
                    'location_lon': end_facility.location_lon
                }
            }
        }
        return JsonResponse(data)
    except DriverJourney.DoesNotExist:
        return JsonResponse({'error': 'Journey not found or not active'}, status=404)


@csrf_exempt
def create_driver_journey(request):
    if request.method == 'POST':
        # Assuming journey_id is passed in the request data
        journey_id = request.POST.get('journey_id')

        try:
            # Retrieve the driver_id based on the journey_id
            journey = get_object_or_404(Journey, id=journey_id)
            driver_id = journey.driver_id
            # print(f"Driver ID: {journey_id}, Type: {type(journey_id)}")

            # Check if driver_id is None or empty
            if not driver_id:
                raise ValueError("Driver not found for the given journey_id")
        except (Journey.DoesNotExist, ValueError) as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=404)

        # Create a new DriverJourney instance
        driver_journey = DriverJourney(driver_id=driver_id, journey_id=journey_id, active=True)
        driver_journey.save()

        return JsonResponse({'success': True, 'message': 'DriverJourney created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def signal_view(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            signal_data = data.get('signal_data')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Trigger the Celery task with the signal_data
        process_signal.delay(data)

        # Return a success response
        return JsonResponse({'message': 'Signal received and processed'})

    # Return a JsonResponse for other HTTP methods
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# class BookViewSet(viewsets.ModelViewSet):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     model = Book
#     serializer_class = BookSerializer
#     queryset = Book.objects.all()


# class BookApiView(APIView):
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#
#     def get(self, request, format=None):
#         allbooks = Book.objects.all().values()
#         return Response({"message": "Book List", "data": allbooks})
#
#     def post(self, request, format=None):
#         Book.objects.create(id=request.data["id"], title=request.data["title"])


# class TeacherListView(APIView):
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#
#     def get(self, request, format=None):
#         teachers = Teacher.objects.prefetch_related('books').all()
#         serializer = TeacherSerializer(teachers, many=True)
#         return Response({"message": "Teachers List", "data": serializer.data})
#
#     def post(self, request, format=None):
#         Teacher.objects.create(id=request.data["id"], title=request.data["name"])


def index(request):
    return render(request, 'index.html')


# views.py

def check_firebase_connection(request):
    if firebase_admin._apps:
        # Firebase Admin SDK is initialized
        return JsonResponse({'status': 'success', 'message': 'Firebase connected'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Firebase not connected'})


def get_firebase_token(request):
    try:
        user_id = 'user_id'  # Provide the user ID for which you want to retrieve the token
        custom_token = auth.create_custom_token(user_id)
        return JsonResponse({'registration_token': custom_token.decode()})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        registration_token = request.POST.get('registration_token', '')
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')

        # Get the FirebaseInitMiddleware instance
        firebase_middleware = FirebaseInitMiddleware(get_response=None)

        # Send the notification
        response = firebase_middleware.send_notification(registration_token, title, body)
        return JsonResponse({'status': 'success', 'response': response})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
