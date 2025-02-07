from django.contrib import admin
from anime.models import Anime, Episode

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 0
    can_delete = False
    readonly_fields = ('number', 'title')
    max_num = 0
    show_change_link = False

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'episode_count')
    search_fields = ('title', 'slug',)
    inlines = [EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'type', 'air_date', 'anime')
    list_filter = ('type', 'anime')
    search_fields = ('title',)
