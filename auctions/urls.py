from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="new_listing"),
    path("listing/<int:list_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("show_watchlist", views.show_watchlist, name="show_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("comment", views.comment, name='comment'),
    path("place_bid", views.place_bid, name="place_bid"),
    path("categories", views.categories, name="categories"),
    path("categories/<slug:slug_name>", views.select_cat, name="select_cat"),
    path("close_auction/<int:list_id>", views.close_auction, name="close_auction"),
    path("win", views.win, name="win"),
    path("lose", views.lose, name="lose")


]
