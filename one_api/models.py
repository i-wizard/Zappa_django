from django.db import models

from user.models import User


class UserFavouriteQuote(models.Model):
    _id = models.CharField(max_length=555, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dialog = models.CharField(max_length=555, null=True, blank=True)
    movie = models.CharField(max_length=555, null=True, blank=True)
    character = models.CharField(max_length=555, null=True, blank=True)

    def __str__(self):
        return self._id


class UserFavoriteCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    _id = models.CharField(max_length=555, null=True, blank=True)
    height = models.CharField(max_length=555, null=True, blank=True)
    race = models.CharField(max_length=555, null=True, blank=True)
    gender = models.CharField(max_length=555, null=True, blank=True)
    birth = models.CharField(max_length=555, null=True, blank=True)
    spouse = models.CharField(max_length=555, null=True, blank=True)
    death = models.CharField(max_length=555, null=True, blank=True)
    realm = models.CharField(max_length=555, null=True, blank=True)
    hair = models.CharField(max_length=555, null=True, blank=True)
    name = models.CharField(max_length=555, null=True, blank=True)
    wikiUrl = models.CharField(max_length=555, null=True, blank=True)
    quotes = models.ManyToManyField(
        UserFavouriteQuote, related_name='character_qoutes')

    def __str__(self):
        return self._id
