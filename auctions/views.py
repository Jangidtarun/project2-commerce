from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Item, Bid, Category, Comment


def index(request):
    items = Item.objects.filter(status=True)
    return render(request, "auctions/index.html", {
        "items": items,
        "categories": Category.objects.all(),
    })

def allitems(request):
    return render(request, "auctions/allitems.html", {
        "items": Item.objects.all(),
        "categories": Category.objects.all()
    })

def myitems(request):
    items = Item.objects.filter(creator=request.user)
    return render(request, "auctions/myitems.html",{
        "items": items,
        "categories": Category.objects.all()    
    })

def listcategory(request):
    if request.method == "POST":
        catg = request.POST["category"]
        items = Item.objects.filter(status=True)
        if catg != "General":
            categorydata = Category.objects.get(cat=catg)
            items = Item.objects.filter(status=True, category = categorydata)
        return render(request, "auctions/index.html", {
            "items": items,
            "categories": Category.objects.all()
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

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        startprice = request.POST["pstart"]
        description = request.POST["description"]
        imgurl = request.POST["imgurl"]
        creator = request.user
        categorydata = Category.objects.get(cat=request.POST["category"])
        
        

        bid = Bid.objects.create(
            bid=startprice,
            user=request.user
        )
        
        Item(
            title=title, 
            creator=creator,
            startingprice=startprice,
            price=bid,
            description=description, 
            img=imgurl, 
            category=categorydata
        ).save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "categories": Category.objects.all()
        })

def dispitem(request, item_id):
    itemdetails = Item.objects.get(pk=item_id)
    if itemdetails.img is None:
        itemdetails.img = "/home/vish/Desktop/project2/commerce/auctions/static/auctions/NoPicAvailable.webp"
    inwatchlist = request.user in itemdetails.watchlist.all()
    allcomments = Comment.objects.filter(item = itemdetails).order_by("-commentime")
    itemdetails.save()
    bidder = itemdetails.price.user
    
    statusmessage = ""
    if request.user == itemdetails.creator:
        if itemdetails.creator == bidder:
            statusmessage = "User did not want to sell the Item"
        else:
            statusmessage = f"Item has been sold to {bidder}"
    else:
        if itemdetails.creator == bidder:
            statusmessage = "User did not want to sell the Item"
        elif request.user == bidder:
            statusmessage = "Congratulations You have wom the Auction"
        else:
            statusmessage = f"Item has been sold to {bidder}"

    return render(request, "auctions/item.html", {
        "details": itemdetails,
        "inwatchlist": inwatchlist,
        "comments": allcomments,
        "ncomments": allcomments.count(),
        "statusmessage": statusmessage
    })

@login_required
def removefromwatchlist(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("dispitem", args=(item_id, )))

@login_required
def addtowatchlist(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("dispitem", args=(item_id, )))

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all(),
        "categories": Category.objects.all()
    })

@login_required
def bidit(request, item_id):
    if request.method == "POST":
        currbid = request.POST["bidprice"]
        message = "Bid placed successfully"
        itemdetails = Item.objects.get(pk=item_id)
        pricetoolowerr = False
        if not currbid:
            pricetoolowerr = True
            message = "Bid update failed: please enter price"
        else:
            if int(currbid) > itemdetails.price.bid:
                newbid = Bid(bid=currbid, user=request.user)
                newbid.save()
                itemdetails.price = newbid
                itemdetails.save()
            else:
                pricetoolowerr = True
                message = "Bid update failed: price too low"
        inwatchlist = request.user in itemdetails.watchlist.all()
        return render(request, "auctions/item.html", {
            "details": itemdetails,
            "inwatchlist": inwatchlist,
            "priceistoolow": pricetoolowerr,
            "message": message
        })

@login_required  
def close(request, item_id):
    itemdetails = Item.objects.get(pk=item_id)
    itemdetails.status = False
    itemdetails.save()
    inwatchlist = request.user in itemdetails.watchlist.all()
    return render(request, "auctions/item.html", {
        "details": itemdetails,
        "inwatchlist": inwatchlist,
    })

@login_required
def commentitem(request, item_id):
    itemdetails = Item.objects.get(pk=item_id)
    inwatchlist = request.user in itemdetails.watchlist.all()
    allcomments = Comment.objects.filter(item = itemdetails).order_by("-commentime")

    if request.method == "POST":
        comment = request.POST["comment"]
        if not comment:
            return render(request, "auctions/item.html", {
                "details": itemdetails,
                "inwatchlist": inwatchlist,
                "comments": allcomments,
                "errormessage": "empty comment cannot be submitted!"
            })
        else:
            newcomment = Comment(
                item = itemdetails,
                auther = request.user,
                message = comment
            )
            newcomment.save()
            allcomments = Comment.objects.filter(item = itemdetails)
            return HttpResponseRedirect(reverse("dispitem", args=(item_id, )))
    else:
        return HttpResponseRedirect(reverse("dispitem", args=(item_id, )))

@login_required
def removefav(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("watchlist"))