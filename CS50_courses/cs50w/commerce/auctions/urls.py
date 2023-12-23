from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("item/<int:listing_id>", views.item, name="item"),
    path('watchlist/', views.watchlist, name='watchlist'),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path('listing/<int:listing_id>/bid/', views.place_bid, name='place_bid'),
    path("add_comment/<int:listing_id>", views.add_comment, name='add_comment'),
    path('close_auction/<int:listing_id>/', views.close_auction, name='close_auction'),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category>/", views.category_listings, name="category_listings"),
]

