from django.db import models


class Pokemon(models.Model):
    """Pokemon model"""
    title = models.CharField(max_length=200)
