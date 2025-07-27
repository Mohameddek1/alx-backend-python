
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
