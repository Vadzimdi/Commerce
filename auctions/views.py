from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def check_if_not_empty(all_objects):
    try:
        c = all_objects[0]
        c = True
    except BaseException:
        c = False
    return c


def index(request):
    list_all = Listing.objects.all()
    c = check_if_not_empty(list_all)
    return render(request, "auctions/index.html", {
        "all_listings": list_all,
        "check": c
    })


def categories(request):
    all_cat = Category.objects.all()
    c = check_if_not_empty(all_cat)
    return render(request, "auctions/categories.html", {
        "all_cat": all_cat,
        "check": c
    })


def look_for_x(user, watch_list):
    if user in watch_list:
        x = True
    else:
        x = False
    return x


def look_for_c(com):
    try:
        c = com[0]
        c = True
    except BaseException:
        c = False
    return c


def check_who_bid(user, owner_bid):
    if user == owner_bid:
        return "Your bid is the current bid."
    else:
        return ""


def check_who_owner(user, owner):
    if user == owner:
        return True
    else:
        return False


def close_auction(request, list_id):
    current_listing = Listing.objects.get(id=list_id)
    current_listing.is_published = False
    current_listing.save()
    return HttpResponseRedirect(reverse("index"))


def win(request):
    pass


def lose(request):
    pass


def select_cat(request, slug_name):
    listing_filter = Listing.objects.filter(category__slug=slug_name)
    return render(request, "auctions/selected_cat.html", {
        "all_listings": listing_filter,
    })


def listing(request, list_id):
    current_listing = Listing.objects.get(id=list_id)
    user = request.user
    z = check_who_bid(user, current_listing.start_bid.user)
    x = look_for_x(user, current_listing.watchlist.all())
    com = current_listing.comments.all()
    c = look_for_c(com)
    y = check_who_owner(user, current_listing.owner)
    return render(request, "auctions/cur_listing.html", {
        "listing": current_listing,
        "user_in_watchlist": x,
        "check": c,
        "comments": com,
        "your_or_not": z,
        "owner": y
    })


def place_bid(request):
    if request.method == "POST":
        current_listing = Listing.objects.get(pk=request.POST['id'])
        user = request.user
        z = check_who_bid(user, current_listing.start_bid.user)
        x = look_for_x(user, current_listing.watchlist.all())
        current_price = current_listing.start_bid.bid
        new_price = int(request.POST['price'])
        com = current_listing.comments.all()
        c = look_for_c(com)
        y = check_who_owner(user, current_listing.owner)

        if new_price < current_price:
            message = "The bid must be at least as large as the current bid"
            return render(request, "auctions/cur_listing.html", {
                "listing": current_listing,
                "user_in_watchlist": x,
                "check": c,
                "comments": com,
                "alert_message": message,
                "your_or_not": z,
                "owner": y
            })
        else:
            current_listing.start_bid.bid = new_price
            current_listing.start_bid.user = request.user
            current_listing.start_bid.save()
            current_listing.bid_count += 1
            current_listing.save()
            z = check_who_bid(user, current_listing.start_bid.user)
            message = "The bid update successful"
            return render(request, "auctions/cur_listing.html", {
                "listing": current_listing,
                "user_in_watchlist": x,
                "check": c,
                "comments": com,
                "successful_message": message,
                "your_or_not": z,
                "owner": y
            })


def show_watchlist(request):
    all_listings = []
    for i in Listing.objects.all():
        print(2)
        if request.user in i.watchlist.all():
            print(1)
            all_listings.append(i)
    return render(request, "auctions/show_watchlist.html", {
        "all_listings": all_listings
    })


def watchlist(request):
    if request.method == "POST":
        current_user = request.user
        current_listing = Listing.objects.get(pk=request.POST['id'])
        if current_user in current_listing.watchlist.all():
            current_listing.watchlist.remove(current_user)
            return HttpResponseRedirect(reverse("listing", args=(request.POST['id'], )))
        else:
            current_listing.watchlist.add(current_user)
            return HttpResponseRedirect(reverse("listing", args=(request.POST['id'], )))


def remove_watchlist(request):
    if request.method == "POST":
        current_user = request.user
        current_listing = Listing.objects.get(pk=request.POST['id'])
        current_listing.watchlist.remove(current_user)
        return HttpResponseRedirect(reverse("show_watchlist"))


def new_listing(request):
    all_category = Category.objects.all()
    current_user = request.user
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        b_user = Bid(user=current_user, bid=request.POST["bid"])
        b_user.save()
        url = request.POST["url"]
        category = Category.objects.get(name=request.POST["category"])
        new_list = Listing(
            title=title,
            content=content,
            start_bid=b_user,
            url=url,
            category=category,
            owner=current_user,
        )
        new_list.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/newlisting.html", {
        "title": "Create new Listing",
        "all_category":  all_category
    })


def comment(request):
    if request.method == "POST":
        current_user = request.user
        current_comment = request.POST['comment']
        com = Comments(text=current_comment, user=current_user)
        com.save()
        current_listing = Listing.objects.get(pk=request.POST['id'])
        current_listing.comments.add(com)
        return HttpResponseRedirect(reverse("listing", args=(request.POST['id'],)))


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
