from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Pokemon model"""
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True, upload_to='pokemon_pictures')

    def __str__(self):
        return self.title
