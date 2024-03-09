from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from app.models import Book
from .serializer import TeacherSerializer, BookSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .tasks import process_signal

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


class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    model = Book
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookApiView(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        allbooks=Book.objects.all().values()
        return Response({"message": "Book List", "data": allbooks})

    def post(self, request, format=None):
        Book.objects.create(id=request.data["id"], title=request.data["title"])


class TeacherListView(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        teachers = Teacher.objects.prefetch_related('books').all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response({"message": "Teachers List", "data": serializer.data})

    def post(self, request, format=None):
        Teacher.objects.create(id=request.data["id"], title=request.data["name"])

def index(request):
    return render(request, 'index.html')

