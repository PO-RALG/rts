from django.urls import path
from otp import views

from .views import generate_otp

urlpatterns = [
    # Other URL patterns...
    path('generate-otp/', generate_otp, name='generate_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),

]
