from django.urls import path

from .views import (RecipesFormView, RecipesFormViewSuccess, index_view,
                    profile_view, purchases_download_view, recipe_edit_view,
                    recipe_view, FollowsView, PurchasesView, FavoritesView,
                    recipe_delete_view, RecipesFormViewDeleteSuccess)

urlpatterns = [
    path("", index_view, name="index"),
    path("creation_recipe/", RecipesFormView.as_view(),
         name="creation_recipe"),
    path("creation_recipe_success/", RecipesFormViewSuccess.as_view(),
         name="creation_recipe_success"),
    path("profile/<str:username>", profile_view,
         name="profile"),
    path("recipe/<str:slug>", recipe_view,
         name="recipe"),
    path("purchases_download/", purchases_download_view,
         name="download"),
    path("<str:slug>/edit/", recipe_edit_view,
         name="recipe_edit"),
    path("<str:slug>/delete/", recipe_delete_view,
         name="recipe_delete"),
    path("delete_recipe_success/", RecipesFormViewDeleteSuccess.as_view(),
         name="delete_recipe_success"),
    path("subscriptions/", FollowsView.as_view(),
         name="subscriptions"),
    path("purchases/", PurchasesView.as_view(),
         name="purchases"),
    path("favorites/", FavoritesView.as_view(),
         name="favorites"),
]
