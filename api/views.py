from django.http import HttpResponse, JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from recipes.models import (Favorites, Follow, IngredientList, Purchases,
                            Recipes, User)


class IngredientsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.method == 'GET' and request.GET['query']:
            ingredients = list(IngredientList.objects.filter(
                title__istartswith=request.GET['query']).values())
        else:
            ingredients = None
        return JsonResponse(ingredients, safe=False)


class FavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        Favorites.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse("succes", safe=False)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        favorite = Favorites.objects.filter(user=request.user, recipe=recipe)
        if favorite:
            favorite.delete()
            return JsonResponse("succes", safe=False)
        return HttpResponse(status=403)


class SubscriptionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        author_id = request.data.get('id')
        Follow.objects.get_or_create(user=request.user, author_id=author_id)
        return JsonResponse("succes", safe=False)

    def delete(self, request, author_id):
        author = get_object_or_404(User, pk=author_id)
        follow = Follow.objects.filter(user=request.user, author=author)
        if follow:
            follow.delete()
            return JsonResponse("succes", safe=False)
        return HttpResponse(status=403)


class PurchasesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        Purchases.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse("succes", safe=False)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        purchase = Purchases.objects.filter(user=request.user, recipe=recipe)
        if purchase:
            purchase.delete()
            return JsonResponse("succes", safe=False)
        return HttpResponse(status=403)


