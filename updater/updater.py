import json
import os
from requests import get, post
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import sys


class Updater:
    def __init__(self):
        self.CURR_PATH = os.path.dirname(os.path.abspath(__file__))
        self.OUTPUT_FILE_NAME = "fillerlist_data.json"
        self.BASE_SCRAPE_URL = "https://www.animefillerlist.com"
        self.SHOWS_SCRAPE_URL = "https://www.animefillerlist.com/shows"
        self.UPLOAD_URL = "https://fillerlist.onrender.com/update/"
        # self.UPLOAD_URL = "http://localhost:8000/update/"
        self.UPLOAD_SECRET_KEY = os.getenv('FILE_UPLOAD_SECRET_KEY')
        self.data = {}


    @staticmethod
    def fetch_anime_list(source):
        soup = BeautifulSoup(get(source).text, "html.parser")

        anime_list = soup.select(".Group a")

        return [{
            "title": anime.text,
            "source": anime.get('href')
        } for anime in anime_list]


    @staticmethod
    async def fetch_anime_detail(session, source):
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

        return detail


    def save(self):
        with open(os.path.join(self.CURR_PATH, self.OUTPUT_FILE_NAME), "w") as f:
            f.write(json.dumps(self.data, indent=4))
    

    def upload(self):
        files = {'file': open(os.path.join(self.CURR_PATH, self.OUTPUT_FILE_NAME),'rb')}
        params = {"key": self.UPLOAD_SECRET_KEY}

        try:
            response = post(self.UPLOAD_URL, files=files, data=params).json()

            if response["status"] == "ok":
                return True
            
            return False
        except Exception as e:
            print(e)
            return False


    async def runner(self):
        print("[INFO] Started")

        self.data["anime"] = self.fetch_anime_list(self.SHOWS_SCRAPE_URL)

        print("[INFO] Fetching list successful!")

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_anime_detail(session, self.BASE_SCRAPE_URL + anime["source"]) \
                    for anime in self.data["anime"]
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for anime, detail in zip(self.data["anime"], results):
                anime.update(detail)
        
        print("[INFO] Fetching details successful!")
        
        self.save()

        print("[INFO] Scrapping successful!")

        if self.upload():
            print("[INFO] Uploading successful!")
            exit(0)
        else:
            print("[ERROR] Uploading failed!")
            exit(1)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(Updater().runner())
