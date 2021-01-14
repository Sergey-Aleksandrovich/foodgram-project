from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (FavoritesAPIView, IngredientsListAPIView,
                       PurchasesAPIView,
                       SubscriptionsAPIView)

router = DefaultRouter()

urlpatterns = [

    path("ingredients/", IngredientsListAPIView.as_view(),
         name="APIingredients"),
    path("favorites/", FavoritesAPIView.as_view(), name="APIfavorites"),
    path("unfavorites/<int:recipe_id>", FavoritesAPIView.as_view(),
         name="APIunfavorites"),
    path("subscriptions/", SubscriptionsAPIView.as_view(),
         name="APIsubscriptions"),
    path("unsubscriptions/<int:author_id>", SubscriptionsAPIView.as_view(),
         name="APIunsubscriptions"),
    path("purchases/", PurchasesAPIView.as_view(),
         name="APIpurchases"),
    path("unpurchases/<int:recipe_id>", PurchasesAPIView.as_view(),
         name="APIunpurchases"),

]
