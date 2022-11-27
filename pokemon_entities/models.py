from django.db import models


class PokemonElementType(models.Model):
    """Pokemon element types"""
    title = models.CharField('стихия', max_length=50)
    img = models.ImageField('изображение', upload_to='element_pictures', null=True)
    strong_against = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name='силён против')

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    """Pokemon model"""
    title = models.CharField('название', max_length=200)
    title_en = models.CharField('название на английском языке', max_length=200, blank=True)
    title_jp = models.CharField('название на японском языке', max_length=200, blank=True)
    description = models.TextField('описание', blank=True)
    photo = models.ImageField('изображение', null=True, upload_to='pokemon_pictures', blank=True)

    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='next_evolutions', verbose_name='Из кого эволюционировал')
    element_type = models.ManyToManyField(PokemonElementType, blank=True, verbose_name='стихия')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Pokemon coordinates"""
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE
    )
    appeared_at = models.DateTimeField('момент появления на карте')
    disappeared_at = models.DateTimeField('момент исчезновления с карты')
    level = models.IntegerField(verbose_name='уровень', null=True, blank=True)
    health = models.IntegerField('здоровье', null=True, blank=True)
    strength = models.IntegerField('сила', null=True, blank=True)
    defence = models.IntegerField('защита', null=True, blank=True)
    stamina = models.IntegerField('выносливость', null=True, blank=True)
