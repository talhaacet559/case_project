from django.apps import AppConfig



class UserserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userservice'

    def ready(self):
        import userservice.signals
