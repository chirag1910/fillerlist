import json
from os import path
from random import choice
from fuzzywuzzy import fuzz


def get_data():
    if not path.exists(file_path):
        return {"data": []}

    with open(file_path, "r") as f:
        return json.loads(f.read())


def update_data(file):
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)


def random(limit=10):
    response = {"data": []}

    count = 0
    while count < limit:
        random_anime = choice(raw_data["anime"])
        if random_anime not in response["data"]:
            random_anime["cover"] = "https://s4.anilist.co/file/anilistcdn/character/large/default.jpg"
            response["data"].append(random_anime)
            count += 1

    return response


def search(keyword):
    response = {"data": [], "keyword": keyword}

    for anime in raw_data["anime"]:
        match = fuzz.partial_ratio(keyword, anime["title"])

        if match > 50:
            anime["match"] = match
            anime["cover"] = "https://s4.anilist.co/file/anilistcdn/character/large/default.jpg"

            response["data"].append(anime)

    response["data"] = sorted(
        response["data"], key=lambda x: x["match"], reverse=True)

    return response


def anime(id):
    for anime in raw_data["anime"]:
        if int(anime["id"]) == int(id):
            return {"data": anime}

    # manual error in website to redirect to error page.
    int('a')


file_path = path.join(path.dirname(
    path.abspath(__file__)), "fillerlist_data.json")

raw_data = get_data()
