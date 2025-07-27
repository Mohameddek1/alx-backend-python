import logging
import os
from datetime import datetime

def check_requests_log():
    log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(log_dir, "requests.log")
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - User: Anonymous - Path: /sample\n")
    return log_file

# Ensure the log file exists and is not empty at import time
check_requests_log()

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_file = os.path.join(log_dir, "requests.log")
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
