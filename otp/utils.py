from twilio.rest import Client
from django.conf import settings
from random import randint
import requests
from requests.auth import HTTPBasicAuth


def send_otp(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid


def send_otp2(phone_number, otp):
    url = "https://apisms.beem.africa/v1/send"

    data = {
        "source_addr": "INFO",
        "encoding": 0,
        "message": f"Your OTP is {otp}",
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": phone_number
            }
        ]
    }

    username = "7b08c6ef970bebab"
    password = "MTY2NDlhMmJlOTI4MzM5OGNmN2RlMTFjODliNWJkMTUyNDBkYjdkZTE5MWYxMDcxMGE0NDVlNzhlM2FiNmRhYg=="

    response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        print("SMS sent successfully!")
    else:
        print("SMS sending failed. Status code:", response.status_code)
        print("Response:", response.text)
