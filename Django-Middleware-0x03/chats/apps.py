from django.apps import AppConfig
from django.core import checks
import os


def check_requests_log(app_configs, **kwargs):
    log_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "requests.log",
    )
    errors = []
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        errors.append(
            checks.Error(
                "requests.log does not exist or is empty.",
                id="chats.E001",
            )
        )
    return errors


class ChatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chats"

    def ready(self):
        checks.register(check_requests_log)
