from recipes import serializers
from recipes.models import Favorites


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorites
        fields = ("user", "recipe")