from django.apps import AppConfig

class JobportalConfig(AppConfig):
    name = 'JobPortal'
    def ready(self):
        import JobPortal.signals
