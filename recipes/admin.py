from django.contrib import admin

from recipes.models import (Favorites, Follow, IngredientList, Ingredients,
                            Purchases, Recipes, Tag)


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'count_favorites')
    search_fields = ('title',)
    list_filter = ('title', 'tags', 'author',)
    empty_value_display = '-пусто-'

    def count_favorites(self, obj):
        result = Favorites.objects.filter(recipe=obj).count()
        return result


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('kind',)
    empty_value_display = '-пусто-'

    def title(self, obj):
        result = obj.kind.title
        return result

    def dimension(self, obj):
        result = obj.kind.dimension
        return result


admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Tag)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientList)
admin.site.register(Favorites)
admin.site.register(Follow)
admin.site.register(Purchases)
