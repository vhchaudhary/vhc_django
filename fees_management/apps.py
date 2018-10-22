from django.apps import AppConfig


class FeesManagementConfig(AppConfig):
    name = 'fees_management'

    def ready(self):
        import fees_management.signals
        import fees_management.cron