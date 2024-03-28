from django.apps import AppConfig
from subprocess import Popen
from threading import Thread
import os
import time
import subprocess
from app.celery import app as celery_app

import firebase_admin
from firebase_admin import credentials


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate('config/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)

        # Start Celery worker in a separate process
        # celery_worker_process = Popen(['celery', '-A', 'app', 'worker', '--loglevel=info'])
        # time.sleep(2)  # Give the worker some time to start
        #
        # # Define a function to check if the Celery worker process is alive
        # def check_celery_worker(timeout=60):
        #     start_time = time.time()
        #     while True:
        #         if celery_worker_process.poll() is not None:
        #             # Celery worker process has exited
        #             break
        #         if time.time() - start_time > timeout:
        #             # Timeout reached, stop checking
        #             break
        #         time.sleep(1)

        # Start a thread to check the status of the Celery worker process
        # thread = Thread(target=check_celery_worker)
        # thread.daemon = True
        # thread.start()
