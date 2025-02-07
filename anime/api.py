from anime.models import Anime

def random(count=10):
    collection = Anime.objects.get_random(count)
    return {"data": [anime.to_dict() for anime in collection]}


def search(keyword):
    collection = Anime.objects.search(keyword)
    return {
        "data": [anime.to_dict() for anime in collection],
        "keyword": keyword
    }


def anime(slug):
    return {"data": Anime.objects.get(slug=slug).to_dict(detailed=True)}
