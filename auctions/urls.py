from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allitems", views.allitems, name="allitems"),
    path("myitems", views.myitems, name="myitems"),
    path("bid/<int:item_id>", views.bidit, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.listcategory, name="category"),
    path("close/<int:item_id>", views.close, name="close"),
    path("item/<int:item_id>", views.dispitem, name="dispitem"),
    path("add/<int:item_id>", views.addtowatchlist, name="add"),
    path("comment/<int:item_id>", views.commentitem, name="comment"),
    path("removefav/<int:item_id>", views.removefav, name="removefav"),
    path("remove/<int:item_id>", views.removefromwatchlist, name="remove"),
]
