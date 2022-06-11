from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal

from .models import User, Item, Bid, Comment
from .forms import ItemForm


def index(request):
    items = Item.objects.all()

    return render(request, "auctions/index.html", { "items": items})


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


def add(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = Item(
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                user=request.user,
                start_price=form.cleaned_data["start_price"],
                category=form.cleaned_data["category"],
                image=form.cleaned_data["image"]
            )
            item.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ItemForm()
        return render(request, "auctions/add.html", {"item_form": form})

def show(request, item_id):
    if request.method == "GET":
        item = Item.objects.get(pk=item_id)
        min_bid = item.start_price + Decimal(0.5)
        if item.bids.all():
            min_bid = item.bids.last().price + Decimal(0.5)
        return render(request, "auctions/show.html", {"item": item, "min_bid": min_bid})

    if request.method == "POST":

        if request.POST["action"] == "close":
            item = Item.objects.get(pk=item_id)
            item.status = "closed"
            item.save()
        
            return render(request, "auctions/show.html", {"item": item, "min_bid": None})

        if request.POST["action"] == "comment":
            comment = Comment(
                text=request.POST["message"],
                user=request.user,
                item=Item.objects.get(pk=item_id)
            )
            comment.save()

            item = Item.objects.get(pk=item_id)
            min_bid = item.start_price + Decimal(0.5)
            if item.bids.all():
                min_bid = item.bids.last().price + Decimal(0.5)
            return render(request, "auctions/show.html", {"item": item, "min_bid": min_bid})


def watchlist(request):
    if request.method == "GET":
        return render(request, "auctions/watchlist.html")
    elif request.method == "POST":
        user = request.user
        item_id = request.POST["item_id"]
        item = Item.objects.get(pk=item_id)
        action = request.POST["action"]

        if action == "add":
            user.watchlist.add(item)

        if action == "remove":
            user.watchlist.remove(item)

        return render(request, "auctions/watchlist.html")


def bid(request):
    if request.method == "POST":
        item_id = request.POST["item_id"]
        amount = request.POST["amount"]

        item = Item.objects.get(pk=item_id)
        bid = Bid(
            item=item,
            price=amount,
            user=request.user
        )
        bid.save()

        return HttpResponseRedirect(reverse("show", args=[item_id]))
