from django.contrib import admin

from . import models


class NotesAdmin(admin.ModelAdmin):
    list_display = ("title", "likes", "created")


admin.site.register(models.Notes, NotesAdmin)
