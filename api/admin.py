from django.contrib import admin

from .models import Game, Creator

admin.site.register(Game)
admin.site.register(Creator)