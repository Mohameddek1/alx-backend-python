
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False) and request.user.is_authenticated else 'Anonymous'
        with open("requests.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        # Debug print to verify middleware is running
        print(f"Logging request: {request.path}")
        return self.get_response(request)


from datetime import time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = time(18, 0, 0)
        end_time = time(21, 0, 0)
        if not (start_time <= current_time <= end_time):
            return HttpResponseForbidden("Access to chats is restricted between 6PM and 9PM only.")
        return self.get_response(request)
