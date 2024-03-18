from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate('config/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
