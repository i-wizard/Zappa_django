from re import search
from rest_framework import serializers

from .models import *
from user.models import User


class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "email"]


class UserFavoriteQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavouriteQuote
        fields = "__all__"


class UserFavoriteCharacterSerializer(serializers.ModelSerializer):
    quotes = UserFavoriteQuoteSerializer(many=True, read_only=True)
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = UserFavoriteCharacter
        fields = "__all__"
