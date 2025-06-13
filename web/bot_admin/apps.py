from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model


class BotAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot_admin'
    # verbose_name = ''

    def ready(self):
        def create_default_superuser(sender, **kwargs):
            User = get_user_model()
            username = settings.DEFAULT_SUPERUSER_USERNAME
            email = settings.DEFAULT_SUPERUSER_EMAIL
            password = settings.DEFAULT_SUPERUSER_PASSWORD
            if username and password and not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email or '', password)

        post_migrate.connect(create_default_superuser, sender=self)
