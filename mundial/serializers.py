from rest_framework import serializers
from .models import Player, Country, Match, PlayerMatch


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("name",)


class PlayerSerializer(serializers.ModelSerializer):
    country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    class Meta:
        model = Player
        fields = ("first_name", "last_name", "age", "position", "country_id")


class MatchSerializer(serializers.ModelSerializer):  # nietestowane
    country_1 = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    country_2 = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    score = Match.score
    match_name = Match.match_name

    class Meta:
        model = Match
        fields = ("country_1", "country_2", "country_1_score", "country_2_score", "score", "match_name")


class PlayerMatchSerializer(serializers.ModelSerializer):
    player_id = serializers.PrimaryKeyRelatedField(read_only=True)
    match_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PlayerMatch
        fields = ("player_id", "match_id", "goals", "assists", "red_cards", "yellow_cards")
