from django.apps import AppConfig


class BookMarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_market'

    def ready(self):
        from book_market import signals
