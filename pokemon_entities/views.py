import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL, popup=''):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
        popup=popup
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lt=localtime(), disappeared_at__gt=localtime()):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url),
            popup=f"""Уровень: {pokemon_entity.level}
            Здоровье: {pokemon_entity.health}
            Сила: {pokemon_entity.strength}
            Защита: {pokemon_entity.defence}
            Выносливость: {pokemon_entity.stamina}
            """
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        img_url = ''
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    img_url = ''
    if requested_pokemon.photo:
        img_url = request.build_absolute_uri(requested_pokemon.photo.url)
    pokemon_on_page = {
        'pokemon_id': requested_pokemon.id,
        'img_url': img_url,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }
    element_types = []
    for element in requested_pokemon.element_type.all():
        element_types.append({'title': element.title, 'img': request.build_absolute_uri(element.img.url),
                              'strong_against': element.strong_against.all()})
    pokemon_on_page.update(element_type=element_types)

    if requested_pokemon.previous_evolution:
        img_url = ''
        if requested_pokemon.previous_evolution.photo:
            img_url = request.build_absolute_uri(requested_pokemon.previous_evolution.photo.url)
        pokemon_on_page.update(previous_evolution={
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': img_url,
            'title_ru': requested_pokemon.previous_evolution.title,
        })
    descendant = requested_pokemon.next_evolutions.all().first()
    if descendant:
        img_url = ''
        if descendant.photo:
            img_url = request.build_absolute_uri(descendant.photo.url)
        pokemon_on_page.update(next_evolutions={
            'pokemon_id': descendant.id,
            'img_url': img_url,
            'title_ru': descendant.title,
        })

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon, appeared_at__lt=localtime(),
                                                       disappeared_at__gt=localtime()):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
