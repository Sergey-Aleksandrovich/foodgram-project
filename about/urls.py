from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('tech/', views.AboutTechView.as_view(), name='tech'),
    path('author/cat', views.AboutCatView.as_view(), name='cat'),
    path('author/i', views.AboutIView.as_view(), name='i')
]