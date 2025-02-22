from django.apps import AppConfig


class LayaliElhelmiaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Layali_elhelmia"
    def ready(self):
        import Layali_elhelmia.signals
