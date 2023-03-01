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
