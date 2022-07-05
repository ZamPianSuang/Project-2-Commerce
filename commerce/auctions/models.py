from asyncio.windows_events import NULL
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import datetime

class User(AbstractUser):
    pass

class Category(models.Model):
    category_name   = models.CharField(max_length=50, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)
    description     = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.id}: {self.category_name}"

class Listing(models.Model):
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField()
    startbid = models.DecimalField(max_digits=7, decimal_places=2)
    currentbid = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", null=True)
    link = models.URLField()
    date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id}: {self.title} | {self.description} | {self.startbid} | {self.currentbid} | {self.category} | {self.date} | {self.creator} | {self.active}"

class Bid(models.Model):
    listingno = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidlistingno")
    bid = models.DecimalField(max_digits=7, decimal_places=2)
    bider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider")

    def __str__(self):
        return f"{self.id}: {self.listingno} | {self.bid} | {self.bider}"

class Comment(models.Model):
    listingno = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentlistingno")
    comments = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.id}: {self.listingno} | {self.comments} | {self.commenter} | {self.date}"

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    list_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_id")

    def __str__(self):
        return f"{self.id}: {self.user_id} | {self.list_id}"
