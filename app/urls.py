from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import views
from app.views import signal_view

router = DefaultRouter()

router.register('book', views.BookViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookApiView.as_view(), name='books'),
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('book/', include(router.urls)),
    path('mobilesignals/', signal_view, name='signal_view'),

]