from asyncio.windows_events import NULL
from csv import unregister_dialect
from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Max

from .models import User, Category, Listing, Bid, Watchlist, Comment


def index(request):    
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.exclude(active=False).all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def CreateListing(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        startbid = request.POST['startbid']
        category_id = request.POST.get('category', False)
        link = request.POST['link']

        category = Category.objects.filter(id=category_id).first()

        lister = User.objects.filter(id=request.user.id).first()

        Listing.objects.create(title=title, description=description, startbid=startbid, 
                    currentbid=startbid, category=category, link=link, creator=lister)

        return redirect("listings", listing_id = Listing.objects.latest('id').id)

    return render(request, "auctions/CreateListing.html", {
        "category": Category.objects.all()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def cate(request, cate_id):
    category = Category.objects.get(id=cate_id)

    return render(request, "auctions/category.html", {
        "cat_list": Listing.objects.filter(category=category).exclude(active=False).all()
    })

def watchlist(request):
    return render(request, "auctions/watchlists.html", {
        "watchlists": Watchlist.objects.filter(user_id=request.user.id).all()
    })

def listings(request, listing_id):

    watchlist = Watchlist.objects.filter(user_id=request.user.id, list_id = listing_id).all()
    list_id = Listing.objects.get(id=listing_id)

    # Check for Watchlist Adding or Removing function & Bid functions
    if request.method == "POST":
        user_id = User.objects.get(id=request.user.id)

        ### Regarding to Watchlist ###
        if request.POST.get("watch_form") == 'Add to Watchlist':
            Watchlist.objects.create(user_id=user_id, list_id=list_id)
            return redirect("listings", listing_id = listing_id)
        elif request.POST.get("watch_form") == 'Remove from Watchlist':
            Watchlist.objects.filter(user_id=user_id, list_id=list_id).delete()
            return redirect("listings", listing_id = listing_id)

        ### Regarding to Bid ###
        elif request.POST.get("bid_form") == 'Close Auction': 
            maxbid = Bid.objects.filter(listingno=list_id).aggregate(Max('bid'))['bid__max']
            bid = Bid.objects.get(listingno=list_id, bid=maxbid)                   # return new owner name
            newowner = User.objects.get(id=bid.bider.id)
            Listing.objects.filter(creator=user_id, id=list_id.id).update(
            winner=newowner, currentbid=maxbid, active=False)                   # Change onwer and no longer active
            return HttpResponseRedirect(reverse("index"))

        elif request.POST.get("bid_form") == 'Place Bid':
            Bid.objects.create(listingno=list_id, bid=request.POST['bid'], bider=user_id)
            Listing.objects.filter(id=listing_id).update(currentbid=request.POST['bid'])
            return redirect("listings", listing_id = listing_id)
            
        ### Regarding to Comment ###
        if request.POST.get("com_form") == 'Post':
            listing = Listing.objects.get(id=listing_id)
            Comment.objects.create(listingno=listing, comments=request.POST['com'], commenter=user_id)
            return redirect("listings", listing_id = listing_id)

    temp = Bid.objects.filter(listingno=listing_id).all()
    bidcount = temp.count()
    currentbid = Listing.objects.get(id=listing_id).currentbid
    maxbid = Bid.objects.filter(listingno=list_id).aggregate(Max('bid'))['bid__max']
    highestbider = None
    
    if bidcount is not 0:
        highestbider = Bid.objects.get(listingno=list_id, bid=maxbid).bider 

    return render(request, "auctions/listings.html", {
        "startbid": Listing.objects.get(id=listing_id).startbid,
        "bidcount": bidcount,
        "currentbid": currentbid,
        "minbid": currentbid+1,
        "highestbider": highestbider,
        "listing": Listing.objects.get(id=listing_id),
        "watchlist": watchlist,
        "comments": Comment.objects.filter(listingno=listing_id).all()
    })

