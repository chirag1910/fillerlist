from django.core.management.base import BaseCommand
from anime.models import Anime, Episode
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import sys
import time


class Command(BaseCommand):
    help = "Command to scrape anime data and update in DB"

    def __init__(self,  *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        self.BASE_SCRAPE_URL = "https://www.animefillerlist.com"
        self.SHOWS_SCRAPE_URL = "https://www.animefillerlist.com/shows"
        
        self.anime_scrap_count_lock = asyncio.Lock()
        self.anime_scrap_count = 0

    def handle(self, *args, **kwargs):
        start_time = time.time()

        print("[INFO] Running command.")

        data = asyncio.run(self.scrape())

        self.update_db(data)

        print(f"[INFO] Running command took {time.time() - start_time:.2f} seconds.")

    async def scrape(self):
        print("[INFO] Scrapping started.")

        data = {}

        async with aiohttp.ClientSession() as session:
            data["anime"] = await self.fetch_anime_list(session, self.SHOWS_SCRAPE_URL)

            print("[INFO] Anime titles scrapped successfully.")

            tasks = [
                self.fetch_anime_detail(session, self.BASE_SCRAPE_URL + anime["source"]) \
                    for anime in data["anime"]
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for anime, detail in zip(data["anime"], results):
                anime.update(detail)
        
        print("[INFO] Scrapping completed successfully.")

        return data

    async def fetch_anime_list(self, session, source):
        response = await session.request("GET", source)
        data = await response.text()

        soup = BeautifulSoup(data, "html.parser")

        anime_list = soup.select(".Group a")

        return [{
            "title": anime.text,
            "source": anime.get('href')
        } for anime in anime_list]

    async def fetch_anime_detail(self, session, source):
        response = await session.request('GET', url=source)
        data = await response.text()
        
        soup = BeautifulSoup(data, "html.parser")

        detail = {}
        detail["description"] = soup.select(".Description p")[0].text

        episode_table_rows = soup.select("tbody tr")

        detail["episodes"] = [{
            "number": row.find("td", {'class': 'Number'}).text,
            "name": row.find("td", {'class': 'Title'}).text,
            "type": row.find("td", {'class': 'Type'}).text,
            "air_date": row.find("td", {'class': 'Date'}).text,
        } for row in episode_table_rows]

        async with self.anime_scrap_count_lock:
            self.anime_scrap_count += 1
            print(f"[INFO] {self.anime_scrap_count} anime(s) has been scrapped.")

        return detail

    def update_db(self, data):
        # Delete all previous data first
        Anime.objects.all().delete()

        print("[INFO] Previous data deleted.")

        animes_to_create = []

        for anime_data in data["anime"]:
            anime = Anime(
                title=anime_data["title"],
                description=anime_data["description"]
            )

            animes_to_create.append(anime)

        Anime.objects.bulk_create(animes_to_create)

        print("[INFO] Anime table updated successfully.")

        # Not using animes_to_create itself because they won't have primary key,
        # due to which they will be treated as unsaved object.
        title_object_map = {anime.title: anime for anime in Anime.objects.all()}

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

        print("[INFO] Episode table updated successfully.")
