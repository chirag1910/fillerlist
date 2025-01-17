from django.db import models
from anime.manager import AnimeManager

class Anime(models.Model):
    id = models.fields.BigAutoField(primary_key=True)
    title = models.fields.CharField(max_length=500)
    description = models.TextField()

    objects = AnimeManager()

    @property
    def episode_count(self):
        return self.episode_set.all().count()
    
    def to_dict(self, detailed=False):
        anime = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'episode_count': self.episode_count
        }

        if detailed:
            anime["episodes"] = [
                episode.to_dict() for episode in self.episode_set.all()
            ]
        
        return anime


class Episode(models.Model):
    EPISODE_TYPES = {
        "anime": "Anime Canon",
        "manga": "Manga Canon",
        "filler": "Filler",
        "mixed": "Mixed Canon/Filler"
    }

    id = models.fields.BigAutoField(primary_key=True)
    number = models.fields.IntegerField()
    title = models.fields.CharField(max_length=400)
    type = models.fields.CharField(max_length=50, choices=EPISODE_TYPES)
    air_date = models.fields.DateField(blank=True, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)

    class Meta:
        ordering = ["number"]

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'title': self.title,
            'type': self.get_type_display(),
            'air_date': self.air_date.strftime('%d-%m-%Y'),
        }
