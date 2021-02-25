from rest_framework import serializers
from roulette_app.models import *


class SpinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spin
        fields = "__all__"

class RoundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ["pk", "user"]

class RoundUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ["pk", "user", "is_finished"]

class RoundDetailSerializer(serializers.ModelSerializer):
    spins = SpinSerializer(many=True)

    class Meta:
        model = Round
        fields = "__all__"
