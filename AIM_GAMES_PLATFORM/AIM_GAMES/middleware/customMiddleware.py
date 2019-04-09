from django.contrib import sessions
from django.utils import translation
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from AIM_GAMES.models import *


class GetLanguage(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.has_key('language'):
            request.session['language'] = 'es-ES'
        language = request.session['language']
        translation.activate(language)


class CountUnreadedMessages(MiddlewareMixin):
    def process_request(self, request):
        count = "0"
        if request.user.is_authenticated:
            user = request.user
            count = str(Message.objects.filter(recipient=user, readed=False).count())
            if int(count) > 99:
                count = "99+"
        request.session['message_count'] = count
        return
