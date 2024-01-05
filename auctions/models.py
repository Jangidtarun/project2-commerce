from datetime import datetime, timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="bidplacer")

    def __str__(self):
        return f"{self.user}: {self.bid}"
    
class Category(models.Model):
    cat = models.CharField(max_length=64, blank=False)

    def __str__(self):
        return f"{self.cat}"

class Item(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    img = models.CharField(max_length=1500, blank=True)
    startingprice = models.IntegerField(default=1)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidprice")
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE, related_name="category")
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    datecreated = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.title}: {self.price.bid}"

class Comment(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE, related_name="commenteditem")
    auther = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="commentwriter")
    message = models.CharField(max_length=120, blank=False)
    commentime = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"commented by {self.auther}"
    