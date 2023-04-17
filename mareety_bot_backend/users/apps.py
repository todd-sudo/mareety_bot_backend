from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "mareety_bot_backend.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import mareety_bot_backend.users.signals  # noqa: F401
        except ImportError:
            pass
