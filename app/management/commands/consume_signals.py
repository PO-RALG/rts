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
        data = json.loads(body)
        signal_data = data.get('signal_data')
        device_imei = data.get('device_imei')

        if signal_data and device_imei:
            DriverAppSignal.objects.create(signal_data=signal_data, device_imei=device_imei)

        message.ack()