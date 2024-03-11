from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Teacher
from .utils import send_otp
from random import randint

from django.utils.decorators import method_decorator
from django.views import View


@csrf_exempt
def generate_otp(request):
    phone_number = request.POST.get('phone_number')
    teacher = Teacher.objects.filter(phone_number=phone_number).first()

    # Console the teacher object
    print("teacher", phone_number)
    if not Teacher:
        return JsonResponse({'error': 'Phone number not found'}, status=400)

    otp = randint(1000, 9999)  # Generate a random 4-digit OTP
    send_otp(teacher.phone_number, otp)  # Send OTP using Twilio

    # Save OTP in the teacher object
    teacher.otp = otp
    teacher.save()

    return JsonResponse({'message': 'OTP sent successfully'})


@method_decorator(csrf_exempt, name='dispatch')
class VerifyOTPView(View):
    @staticmethod
    def post(request):
        phone_number = request.POST.get('phone_number')
        otp_entered = request.POST.get('otp')

        if not phone_number or not otp_entered:
            return JsonResponse({'error': 'Phone number or OTP not provided'}, status=400)

        teacher = Teacher.objects.filter(phone_number=phone_number, otp=otp_entered).first()
        # print("teacher", teacher)

        if not teacher:
            return JsonResponse({'error': 'Incorrect OTP'}, status=400)

        # Clear OTP after successful verification
        teacher.otp = None
        teacher.save()

        # Return teacher information
        return JsonResponse({
            'message': 'OTP verified successfully',
            'teacher': {
                'id': teacher.id,
                'name': teacher.name,
                'phone_number': teacher.phone_number,
            }
        })
