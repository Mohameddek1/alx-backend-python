import logging
import os
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set log file path to project directory
        log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file = os.path.join(log_dir, "requests.log")
        # Only configure logging if not already configured
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                filename=log_file,
                level=logging.INFO,
                format='%(message)s'
            )

    def __call__(self, request):
        user = request.user if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False) and request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response
