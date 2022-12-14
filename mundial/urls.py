from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="mundial-home"),
    path("about/", views.About.as_view(), name="mundial-about"),
    path("player/", views.Player.as_view(), name="mundial-player"),
    path("player/<int:pk>", views.Player.as_view(), name="mundial-player-id"),
    path("player/<int:player_id>/stats", views.PlayerStats.as_view(), name="mundial-player-stats"),
    path("country/", views.Country.as_view(), name="mundial-country"),
    path("country/<int:pk>", views.Country.as_view(), name="mundial-country-id"),
    path("country/<int:country_id>/stats", views.CountryStats.as_view(), name="mundial-country-stats"),
    path("match/", views.Match.as_view(), name="mundial-match"),
    path("match/<int:pk>", views.Match.as_view(), name="mundial-match-id"),
]
