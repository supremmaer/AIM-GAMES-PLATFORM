from django.contrib import sessions
from django.utils import translation
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class GetLanguage(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.has_key('language'):
            request.session['language'] = 'es-ES'
        language = request.session['language']
        translation.activate(language)

