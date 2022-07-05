from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.CreateListing, name="CreateListing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("categories", views.categories, name="categories"),
    path("cate/<int:cate_id>", views.cate, name="cate"),
    path("watchlists", views.watchlist, name="watchlist"),
]
