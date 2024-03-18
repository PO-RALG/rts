import os
import firebase_admin
from firebase_admin import credentials, messaging

class FirebaseInitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/serviceAccountKey.json'))
            firebase_admin.initialize_app(cred)
        self.messaging = messaging

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response

    def send_notification(self, registration_token, title, body):
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=registration_token,
        )
        response = self.messaging.send(message)
        return response
