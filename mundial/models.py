from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Countries"


class Positions(models.TextChoices):  # TextChoices outside Player model class so Meta can access
    GOALKEEPER = "Goalkeeper"
    DEFENDER = "Defender"
    MIDFIELDER = "Midfielder"
    STRIKER = "Striker"


class Player(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50, choices=Positions.choices)
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_position_valid",
                check=models.Q(position__in=Positions.values),  # check if positions is valid on database level
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Match(models.Model):
    country_1 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_1")
    country_2 = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_2")
    country_1_score = models.IntegerField()
    country_2_score = models.IntegerField()

    @property
    def score(self):
        return f"{self.country_1_score}:{self.country_2_score}"

    @property
    def match_name(self):
        return f"{self.country_1} vs {self.country_2}"

    def __str__(self):
        return f"{self.country_1} vs {self.country_2}"

    class Meta:
        verbose_name_plural = "Matches"


class PlayerMatch(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    yellow_cards = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    red_cards = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    goals = models.IntegerField()
    assists = models.IntegerField()

    def __str__(self):
        return f"{self.player} in match {self.match}"

    class Meta:
        verbose_name_plural = "PlayerMatch"
