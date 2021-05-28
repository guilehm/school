from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school.core'

    def ready(self):
        import school.core.signals  # noqa
