from django.db import models
from django.contrib.auth import get_user_model


class TodoQueryset(models.QuerySet):
    def get_for_user(self, user):
        return self.filter(user=user)


class Todo(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TodoQueryset.as_manager()

    def __str__(self) -> str:
        return self.title
