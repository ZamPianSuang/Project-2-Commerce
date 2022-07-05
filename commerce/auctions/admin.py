from django.contrib import admin
from . models import User, Category, Listing, Bid, Comment, Watchlist

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('id', 'category_name', 'slug')
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "startbid", "currentbid", "category", "date", "creator", "winner", "active")
class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listingno", "bid", "bider")
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listingno", "comments", "commenter", "date")
class WatchlistAdmin(admin.ModelAdmin):
    list_display =("id", "user_id", "list_id")    

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)