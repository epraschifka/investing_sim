from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = "my_app"

    def ready(self):
        from priceUpdater import updater
        updater.start()