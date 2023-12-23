from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="article"),
    path("search/", views.search, name="search"),
    path("new page/", views.new_page, name="new_page"),
    path("wki/new_entry", views.entry_created, name="entry_created"),
    path("edit_page/<entry_name>", views.edit_page, name="edit_page"),
    path("randon/", views.random_page, name="random_page")
]
