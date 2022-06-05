from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Item(models.Model):
    CATEGORIES = [
        ("book", "Books"),
        ("video", "Videos"),
        ("audio", "Audios"),
        ("img", "Images"),
        ("other", "Other")
    ]

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    start_price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=64, choices=CATEGORIES, default="book")
    image = models.CharField(max_length=256, blank=True)


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="bids")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")


class Comment(models.Model):
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
