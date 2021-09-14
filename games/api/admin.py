from django.contrib import admin


from .models import Game, Creator, GameCategory

admin.site.register(Game)
admin.site.register(Creator)
admin.site.register(GameCategory)

