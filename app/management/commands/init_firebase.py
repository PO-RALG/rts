# myapp/management/commands/init_firebase.py

from django.core.management.base import BaseCommand
import firebase_admin
from firebase_admin import credentials


class Command(BaseCommand):
    help = 'Initialize Firebase Admin SDK'

    def handle(self, *args, **kwargs):
        cred = credentials.Certificate('.config/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
