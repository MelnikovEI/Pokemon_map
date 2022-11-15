from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Pokemon model"""
    title = models.CharField(max_length=200)
    photo = models.ImageField(null=True, upload_to='pokemon_pictures')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Pokemon coordinates"""
    lat = models.FloatField()
    lon = models.FloatField()
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE
    )
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
