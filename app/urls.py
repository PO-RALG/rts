from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views
from app.views import signal_view, create_driver_journey

router = DefaultRouter()

# router.register('book', views.BookViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    # path('books/', views.BookApiView.as_view(), name='books'),
    # path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    # path('book/', include(router.urls)),
    path('mobilesignals/', signal_view, name='signal_view'),
    path('journey/<str:driver_id>/', views.get_journey_by_driver_id, name='get_journey_by_driver_id'),
    path('create_driver_journey/', create_driver_journey, name='create_driver_journey'),
    path('check_firebase_connection/', views.check_firebase_connection, name='check_firebase_connection'),
    # path('send_notification/', views.send_notification, name='send_notification'),
    path('get_firebase_token/', views.get_firebase_token, name='get_firebase_token'),

]