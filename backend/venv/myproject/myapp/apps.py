from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = "myapp"

    def ready(self):
        from priceUpdater import updater
        updater.start()
