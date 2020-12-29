from django.urls import path

from .views import RecipesFormView, ingredients_list, \
    RecipesFormViewSuccess, FavoriteView, FollowView, recipe_view, \
    profile_view, PurchasesView, purchases_download_view, index_view, \
    recipe_edit_view

urlpatterns = [
    path("", index_view, name="index"),
    path("creation_recipe/", RecipesFormView.as_view(),
         name="creation_recipe"),
    path("ingredients/", ingredients_list, name="ingredients"),
    path("creation_recipe_success/", RecipesFormViewSuccess.as_view(),
         name="creation_recipe_success"),
    path("favorites", FavoriteView.as_view(), name="favorites"),
    path("unfavorites/<int:recipe_id>", FavoriteView.as_view(),
         name="unfavorites"),
    path("profile/<str:username>", profile_view,
         name="profile"),
    path("subscriptions", FollowView.as_view(),
         name="subscriptions"),
    path("unsubscriptions/<int:author_id>", FollowView.as_view(),
         name="unsubscriptions"),
    path("recipe/<str:slug>", recipe_view,
         name="recipe"),
    path("purchases", PurchasesView.as_view(),
         name="purchases"),
    path("unpurchases/<int:recipe_id>", PurchasesView.as_view(),
         name="unpurchases"),
    path("purchases_download", purchases_download_view,
         name="download"),
    path("<str:slug>/edit/", recipe_edit_view,
         name="recipe_edit"),
]
