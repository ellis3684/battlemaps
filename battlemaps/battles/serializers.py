from rest_framework_gis import serializers
from .models import Battle


class BattleSerializer(serializers.ModelSerializer):
    point = serializers.GeometryField()

    class Meta:
        model = Battle
        fields = '__all__'
