from AIM_GAMES.models import MyModel


def messagesCount(request):
    context_data = dict()
    count = 0
    if request.user.is_authenticated:
        user = request.user
        count = Message.objects.filter(recipient=user).count()
    context_data['message_count'] = count
    return context_data