from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from .filters import NearestBattlesFilter
from .models import Battle
from .serializers import BattleSerializer


class BattleAPIView(ListAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
    distance_ordering_filter_field = 'point'
    filter_backends = (NearestBattlesFilter,)


class BattleTemplateView(TemplateView):
    template_name = 'battles/index.html'
