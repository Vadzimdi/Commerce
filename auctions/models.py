from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")
    bid = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bid}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    start_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, blank=True, null=True, related_name="starting_bid")
    is_published = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=500)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name="listing_owner")
    watchlist = models.ManyToManyField('User', blank=True, related_name="watch_list")
    comments = models.ManyToManyField('Comments', blank=True, related_name="comments")

    def __str__(self):
        return f"{self.title}, {self.start_bid}, {self.is_published}, {self.category}"


class Comments(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")


