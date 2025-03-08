from .models import Market, Genre
from modeltranslation.translator import TranslationOptions, register


@register(Market)
class MarketTranslationOptions(TranslationOptions):
    fields = ('market_name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('genre_name',)
