from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    likes = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notes"
    )  # Assuming you want to link notes to a user
    is_public = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.title
    #
    # class Meta:
    #     ordering = ["-created"]  # Newest notes first
    #     verbose_name_plural = "Notes"  # Custom plural name for the model
