from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Pokemon model"""
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
