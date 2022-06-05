from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
    item = Item.objects.get(pk=item_id)
    return render(request, "auctions/show.html", {"item": item})
