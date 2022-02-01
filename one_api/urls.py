from django.urls import path

from .views import *

urlpatterns = [
    path("characters", CharacterView.as_view(), name="character"),
    path("characters/<str:pk>", add_favorite_character, name="character"),
    path("characters/<str:pk>/quotes", QuoteView.as_view(), name="quote"),
    path("characters/<str:pk>/quotes/<str:quote_id>/favorites",
         add_favorite_quote, name="add_quote"),
    path('favorites', GetFavorites.as_view(), name="favorites")
]
