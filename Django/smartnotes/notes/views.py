from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notes
from .forms import NotesForm


def add_like(request, pk):
    if request.method == "POST":
        note = get_object_or_404(Notes, pk=pk)
        note.likes += 1
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    raise Http404("Invalid request method")


def change_visibility_view(request, pk):
    if request.method == "POST":
        note = get_object_or_404(Notes, pk=pk)
        note.is_public = not note.is_public  # Toggle public status
        note.save()
        return HttpResponseRedirect(reverse("notes.detail", args=(pk,)))
    raise Http404("Invalid request method")


class NotesDeleteView(DeleteView):
    model = Notes
    success_url = "/smart/notes"  # Redirect to notes list after deletion
    template_name = "notes/notes_delete.html"  # Template for confirmation


class NotesUpdateView(UpdateView):
    model = Notes
    success_url = "/smart/notes"  # Redirect to notes list after creation
    form_class = NotesForm  # Assuming you have a form class defined in forms.py


class NotesCreateView(CreateView):
    model = Notes
    success_url = "/smart/notes"  # Redirect to notes list after creation
    form_class = NotesForm  # Assuming you have a form class defined in forms.py

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user  # Set the user to the logged-in user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    template_name = "notes/notes_list.html"
    context_object_name = "notes"
    ordering = ["-created"]  # Newest notes first
    login_url = "/admin"  # Redirect to admin login if not logged in

    def get_queryset(self):
        # Filter notes by the logged-in user
        # return Notes.objects.filter(user=self.request.user).order_by("-created")
        return self.request.user.notes.all()


class NotesDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    context_object_name = "note"


class NotesPublicDetailView(DetailView):
    model = Notes
    context_object_name = "note"
    queryset = Notes.objects.filter(is_public=True)  # Only show public notes


class NotesLikedListView(ListView):
    model = Notes
    template_name = "notes/notes_list.html"
    context_object_name = "notes"
    queryset = Notes.objects.filter(likes__gt=1).order_by("-created")
