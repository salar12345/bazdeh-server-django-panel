from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bzsdp.app'

    def get_models(self, include_auto_created=False, include_swapped=False):
        return super().get_models(include_auto_created, include_swapped)
