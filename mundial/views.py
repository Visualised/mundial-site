from django.db.models import Sum
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
from .models import Player as PlayerModel
from .models import Country as CountryModel
from .models import Match as MatchModel
from .models import PlayerMatch as PlayerMatchModel
from .models import Stadium as StadiumModel
from .serializers import PlayerSerializer, CountrySerializer, MatchSerializer, PlayerMatchSerializer, StadiumSerializer


class Home(mixins.ListModelMixin, GenericAPIView):

    serializer_class = MatchSerializer
    queryset = MatchModel.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        content = {
            "match_list": self.list(request).data,
        }

        return Response(content, template_name="mundial/home.html")


class About(APIView):

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):

        return Response(template_name="mundial/about.html")


class AbstractCRUDView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericAPIView,
):

    serializer_class = None
    queryset = None

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request, pk=None):
        if pk:
            return HttpResponse(f"Please use PATCH method to update {self.queryset.model.__name__} data.", status=400)
        return self.create(request)

    def put(self, request, pk=None):
        if not pk:
            return HttpResponse(
                f"Please specify {self.queryset.model.__name__} ID in order to update data.", status=400
            )
        return self.update(request)

    def patch(self, request, pk=None):
        if not pk:
            return HttpResponse(
                f"Please specify {self.queryset.model.__name__} ID in order to update data.", status=400
            )
        return self.partial_update(request)

    def delete(self, request, pk=None):
        if not pk:
            return HttpResponse(
                f"Please specify {self.queryset.model.__name__} ID in order to delete data.", status=400
            )
        return self.destroy(request)


class Stadium(AbstractCRUDView):
    serializer_class = StadiumSerializer
    queryset = StadiumModel.objects.all()


class Player(AbstractCRUDView):

    serializer_class = PlayerSerializer
    queryset = PlayerModel.objects.all()


class Country(AbstractCRUDView):

    serializer_class = CountrySerializer
    queryset = CountryModel.objects.all()


class Match(AbstractCRUDView):

    serializer_class = MatchSerializer
    queryset = MatchModel.objects.all()


class PlayerStats(APIView):
    def get(self, request, player_id=None):
        try:
            if player_id:
                query = PlayerMatchModel.objects.filter(player_id=player_id).all()
                serializer = PlayerMatchSerializer(query[0])
                return Response(serializer.data)
        except IndexError:
            return HttpResponse("Player not found", status=404)


class CountryStats(APIView):
    def get(self, request, country_id=None):
        if country_id:
            does_country_exist = CountryModel.objects.get(pk=country_id) or 0

            if does_country_exist:
                goal_count = self.get_country_goal_count(country_id)
                match_count = self.get_country_match_count(country_id)
                yellow_cards_count = self.get_country_yellow_cards_count(country_id)
                red_cards_count = self.get_country_red_cards_count(country_id)

                body = {
                    "matches": match_count,
                    "goals": goal_count,
                    "avg_goals_per_match": goal_count / match_count if match_count else 0,
                    "yellow_cards_count": yellow_cards_count,
                    "red_cards_count": red_cards_count,
                }

                return Response(body, status=200)

        return HttpResponse("Not found", status=404)

    @staticmethod
    def get_country_goal_count(country_id):
        host_goals = (
            MatchModel.objects.filter(country_1_id=country_id).aggregate(Sum("country_1_score"))["country_1_score__sum"]
            or 0
        )
        away_goals = (
            MatchModel.objects.filter(country_2_id=country_id).aggregate(Sum("country_2_score"))["country_2_score__sum"]
            or 0
        )

        goal_count = host_goals + away_goals

        return goal_count

    @staticmethod
    def get_country_match_count(country_id):
        country_matches_host_count = MatchModel.objects.filter(country_1_id=country_id).count()
        country_matches_away_count = MatchModel.objects.filter(country_2_id=country_id).count()

        match_count = country_matches_host_count + country_matches_away_count

        return match_count

    @staticmethod
    def get_country_yellow_cards_count(country_id):
        country_yellow_cards_count = (
            PlayerMatchModel.objects.filter(player__country=country_id).aggregate(Sum("yellow_cards"))[
                "yellow_cards__sum"
            ]
            or 0
        )

        return country_yellow_cards_count

    @staticmethod
    def get_country_red_cards_count(country_id):
        country_red_cards_count = (
            PlayerMatchModel.objects.filter(player__country=country_id).aggregate(Sum("red_cards"))["red_cards__sum"]
            or 0
        )

        return country_red_cards_count
