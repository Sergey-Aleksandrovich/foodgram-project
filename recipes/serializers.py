from rest_framework import serializers

from .models import IngredientList


class IngredientsModelSerializer(serializers.Serializer):
    class Meta:
        model = IngredientList
        fields = "__all__"



