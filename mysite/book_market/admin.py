from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class GeneralMedia:
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Market)
class MarketAdmin(TranslationAdmin, GeneralMedia):
    pass


@admin.register(Genre)
class GenreAdmin(TranslationAdmin, GeneralMedia):
    pass


admin.site.register(UserProfile)
admin.site.register(Branch)
admin.site.register(Contact)
admin.site.register(Subscription)
admin.site.register(Book)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
