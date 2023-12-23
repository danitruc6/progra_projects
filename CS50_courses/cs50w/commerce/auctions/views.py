from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Max

from .models import * 


def index(request):
    # the following annotate functions, helps us to pass the highest bid to the index html, saving us to filter or add the Bid model
    listings = Listing.objects.all().annotate(highest_bid=Max('bid__amount'))
    closed_listings = Listing.objects.filter(closed=True) 
    return render(request, "auctions/index.html", {
        'listings':listings,
        'closed_listings':closed_listings,
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

def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")
    else:
        new_title=request.POST['title']
        new_description = request.POST['description']
        new_price = request.POST['price']
        new_category = request.POST['category']
        new_image = request.POST['image_url']
        listed_by=request.user
        new_entry = Listing(title=new_title, starting_bid=new_price, description=new_description, url_image=new_image, category=new_category, user=listed_by)
        new_entry.save()
        return index(request)

def item(request, listing_id):
    content=Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=content)
    bid = Bid.objects.filter(listing=content)
    watchlist_item = None
    if request.user.is_authenticated:
        try:
            watchlist_item = Watchlist.objects.get(user=request.user, listing_id=listing_id)
        except Watchlist.DoesNotExist:
            watchlist_item = None
    if request.method == "GET":
        return render(request, "auctions/listing.html",{
            "content":content,
            "watchlist_item": watchlist_item,
            "comments":comments,
            "bid":bid
            })
    # POST methot
    # else:
    #     placed_bid = request.POST['new_bid']
    #     if placed_bid > content.starting_bid:
    #         new_bid_entry = Bid(amount=placed_bid, listing=content, user=request.user)
    #         new_bid_entry.save()
    #         # display error
    #         return HttpResponseRedirect(reverse("index"))
    #     else:
    #         return HttpResponseRedirect(reverse("index"))


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    current_bid = listing.starting_bid
    if Bid.objects.filter(listing=listing).exists():
        current_bid = Bid.objects.filter(listing=listing).order_by('-amount').first().amount
    if request.method == "POST":
        amount = request.POST["new_bid"]
        if int(amount) > current_bid and int(amount) > listing.starting_bid:
            bid = Bid(amount=amount, listing=listing, user=request.user)
            bid.save()
            listing.qty_bids += 1
            listing.save()
            return redirect(reverse('item', args=[listing_id]))
        else:
            return render(request, "auctions/bid_error.html", {
                "current_bid": current_bid,
                "listing": listing
            })
    else:
        return redirect(reverse('item', args=[listing_id]))


@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist_item = Watchlist(user=request.user, listing=listing)
    watchlist_item.save()
    return HttpResponseRedirect(reverse("item", args=[listing_id]))

@login_required
def remove_from_watchlist(request, listing_id):
    try:
        watchlist_item = Watchlist.objects.get(user=request.user, listing_id=listing_id)
        watchlist_item.delete()
    except Watchlist.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse("item", args=[listing_id]))

@login_required
@require_POST
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    comment = request.POST["comment"]
    new_comment = Comment(comment=comment, listing=listing, user=request.user)
    new_comment.save()


    return redirect('item', listing_id)

    
@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Only allow the user who created the listing to close the auction
    if request.user == listing.user:
        if listing.bid_set.all():
            highest_bid = listing.bid_set.last()
            listing.winner = highest_bid.user.username
            listing.closed = True
            listing.save()
        return redirect('item', listing_id=listing.id)
    else:
        # Return a 403 error if the user is not the creator of the listing
        return HttpResponseForbidden()

def category_listings(request, category):
    listings = Listing.objects.filter(category=category, closed=False)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })


def categories(request):
    categories = Listing.objects.filter(closed=False).values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })