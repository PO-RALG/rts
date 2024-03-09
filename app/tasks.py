# tasks.py
from celery import shared_task
import json

from kombu import Exchange, Queue, Connection

signals = Exchange('signals', 'direct', durable=True)
signal_queue = Queue('signal-queue', exchange=signals, routing_key='signal-queue')
def send_to_rabbit(signal_data):
    with Connection('amqp://guest:guest@localhost//') as conn:
        producer = conn.Producer(serializer='json')
        producer.publish(
            signal_data,
            exchange=signals,
            routing_key='signal-queue',
            declare=[signal_queue]
        )

@shared_task
def process_signal(signal_data):
    # Process the signal data here
    # For example, save the signal to your signal table
    print(f"Received signal: {signal_data}")
    # save_signal_to_table(signal_data)
    # Send the signal data to RabbitMQ
    send_to_rabbit(signal_data)