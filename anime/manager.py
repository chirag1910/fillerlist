from django.db import models
from fuzzywuzzy import fuzz

class AnimeManager(models.Manager):
    def get_random(self, count=10):        
        return self.all().order_by('?')[:count]

    def search(self, keyword):
        result = []

        id_match_map = {}

        for anime in self.all():
            match = fuzz.partial_ratio(keyword, anime.title)

            if match > 50:
                id_match_map[anime.id] = match
                result.append(anime)
        
        result.sort(key=lambda anime: id_match_map[anime.id],
                    reverse=True)

        return result
