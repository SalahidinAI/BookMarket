from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(Market)
admin.site.register(Branch)
admin.site.register(Contact)
# admin.site.register(Event)
admin.site.register(Subscription)
admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)
