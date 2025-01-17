from anime.models import Anime, Episode
import json


def update_data(file):
    data = json.loads(file.read().decode('utf-8'))

    # Delete all previous data first
    Anime.objects.all().delete()

    animes_to_create = []

    for anime_data in data["anime"]:
        anime = Anime(
            title=anime_data["title"],
            description=anime_data["description"]
        )

        animes_to_create.append(anime)

    Anime.objects.bulk_create(animes_to_create)

    title_object_map = {anime.title: anime for anime in animes_to_create}

    episode_to_create = []

    for anime_data in data["anime"]:
        anime = title_object_map[anime_data["title"]]

        for episode_data in anime_data["episodes"]:
            episode = Episode(
                number=episode_data["number"],
                title=episode_data["name"],
                type=episode_data["type"].split(" ")[0].lower(),
                air_date=episode_data["air_date"] or None,
                anime=anime
            )

            episode_to_create.append(episode)

    Episode.objects.bulk_create(episode_to_create)


def random(count=10):
    collection = Anime.objects.get_random(count)
    return {"data": [anime.to_dict() for anime in collection]}


def search(keyword):
    collection = Anime.objects.search(keyword)
    return {
        "data": [anime.to_dict() for anime in collection],
        "keyword": keyword
    }


def anime(id):
    return {"data": Anime.objects.get(id=int(id)).to_dict(detailed=True)}
