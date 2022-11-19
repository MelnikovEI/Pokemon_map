from django.db import models  # noqa F401


class Pokemon(models.Model):
    """Pokemon model"""
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(null=True, upload_to='pokemon_pictures')

    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='next_evolution')

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
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
