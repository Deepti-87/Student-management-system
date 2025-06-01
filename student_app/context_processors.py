from .models import Message

def recent_message_count(request):
    return {
        'message_count': Message.objects.count()
    }
