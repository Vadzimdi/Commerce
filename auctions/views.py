from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "all_listings": Listing.objects.all()
    })


def listing(request, list_id):
    current_listing = Listing.objects.get(id=list_id)
    user = request.user
    if user in current_listing.watchlist.all():
        x = True
    else:
        x = False
    com = current_listing.comments.all()
    try:
        c = com[0]
        c = True
    except BaseException:
        c = False

    return render(request, "auctions/cur_listing.html", {
        "listing": current_listing,
        "user_in_watchlist": x,
        "check": c,
        "comments": com
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
            category=category
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
