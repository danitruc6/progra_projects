from django.urls import path

from . import views


urlpatterns = [
    path("notes", views.NotesListView.as_view(), name="notes.list"),
    path("notes/<int:pk>", views.NotesDetailView.as_view(), name="notes.detail"),
    path("liked_notes", views.NotesLikedListView.as_view(), name="liked_list"),
    path("notes/<int:pk>/edit", views.NotesUpdateView.as_view(), name="notes.update"),
    path("notes/<int:pk>/delete", views.NotesDeleteView.as_view(), name="notes.delete"),
    path("notes/<int:pk>/add_like", views.add_like, name="notes.add_like"),
    path(
        "notes/<int:pk>/change_visibility",
        views.change_visibility_view,
        name="notes.change_visibility",
    ),
    path("notes/new", views.NotesCreateView.as_view(), name="notes.new"),
    path(
        "notes/<int:pk>/share",
        views.NotesPublicDetailView.as_view(),
        name="notes.share",
    ),
]
