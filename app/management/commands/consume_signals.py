from django.core.management.base import BaseCommand
from kombu import Connection, Exchange, Queue
from app.models import DriverAppSignal
import json


class Command(BaseCommand):
    help = 'Consumes signals from RabbitMQ and saves them to the database'

    def handle(self, *args, **options):
        with Connection('amqp://guest:guest@localhost//') as conn:
            exchange = Exchange('signals', type='direct')
            queue = Queue('signal-queue', exchange, routing_key='signal-queue')
            consumer = conn.Consumer(queue, callbacks=[self.process_signal])
            consumer.consume()

            while True:
                conn.drain_events()

    def process_signal(self, body, message):
        print('Received', type(body))
        data = body
        device_id = data.get('device_id')
        device_imei = data.get('device_imei')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude and longitude and device_imei and device_id:
            DriverAppSignal.objects.create(device_id=device_id, device_imei=device_imei,
                                           latitude=latitude, longitude=longitude)
        message.ack()
