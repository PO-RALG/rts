from twilio.rest import Client
from django.conf import settings
from random import randint

def send_otp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid