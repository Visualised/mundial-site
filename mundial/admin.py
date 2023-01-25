from django.contrib import admin
from .models import Country, Player, Match, PlayerMatch, Stadium


MODELS_TO_REGISTER = [
    Country,
    Player,
    Match,
    PlayerMatch,
    Stadium,
]
admin.site.register(MODELS_TO_REGISTER)
