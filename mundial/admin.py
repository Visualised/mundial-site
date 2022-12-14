from django.contrib import admin
from .models import Country, Player, Match, PlayerMatch


MODELS_TO_REGISTER = [
    Country,
    Player,
    Match,
    PlayerMatch,
]
admin.site.register(MODELS_TO_REGISTER)
