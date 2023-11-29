from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = "myapp"

    def ready(self):
        from forecastUpdater import updater

        updater.start()
