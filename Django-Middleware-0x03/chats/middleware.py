class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        # Only check for authenticated users
        if user and user.is_authenticated:
            # Check for 'admin' or 'moderator' role
            role = getattr(user, 'role', None)
            if role not in ('admin', 'moderator'):
                return HttpResponseForbidden('You do not have permission to perform this action.')
        else:
            # If not authenticated, block access
            return HttpResponseForbidden('Authentication required.')
        return self.get_response(request)

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

import time as pytime
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    # Store IP address and their message timestamps
    ip_message_times = {}
    MESSAGE_LIMIT = 5
    TIME_WINDOW = 60  # seconds

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only limit POST requests (e.g., sending messages)
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = pytime.time()
            times = self.ip_message_times.get(ip, [])
            # Remove timestamps older than TIME_WINDOW
            times = [t for t in times if now - t < self.TIME_WINDOW]
            if len(times) >= self.MESSAGE_LIMIT:
                return JsonResponse({'error': 'Message rate limit exceeded. Max 5 messages per minute.'}, status=429)
            times.append(now)
            self.ip_message_times[ip] = times
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

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
