from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '')
        message = request.POST.get('message', '')

        # Modify the group name to include the ID
        group_name = f"user_{user_id}"

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "notification.message",
                "message": message,
            }
        )
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
