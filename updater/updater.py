import json
import os
from requests import get, post
from bs4 import BeautifulSoup

try:
    CURR_PATH = os.path.dirname(os.path.abspath(__file__))

    data_string = {
        "source": "https://www.animefillerlist.com/",
        "anime": []
    }

    anime_list = BeautifulSoup(get(
        "https://www.animefillerlist.com/shows").text, "html.parser").select(".Group a")
    anime_id = 1

    # anime names
    for anime in anime_list:
        source_link = f"https://www.animefillerlist.com{anime.get('href')}"
        data_string["anime"].append(
            {"id": anime_id, "title": anime.text, "source_link": source_link})
        anime_id += 1

    # anime data
    for anime in data_string["anime"]:
        soup = BeautifulSoup(get(anime["source_link"]).text, "html.parser")

        anime["description"] = soup.select(".Description p")[0].text
        anime["episodes"] = []

        episode_table_rows = soup.select("tbody tr")
        for row in episode_table_rows:
            ep_info = {
                "number": row.find("td", {'class': 'Number'}).text,
                "name": row.find("td", {'class': 'Title'}).text,
                "type": row.find("td", {'class': 'Type'}).text,
                "air_date": row.find("td", {'class': 'Date'}).text,
            }
            anime["episodes"].append(ep_info)

        print(anime["id"], anime["title"])

    with open(os.path.join(CURR_PATH, "fillerlist_data.json"), "w") as f:
        f.write(json.dumps(data_string, indent=4))

    print("Done! Now uploading")

except Exception as e:
    exit(1)

files = {'file': open(os.path.join(CURR_PATH, "fillerlist_data.json"), 'rb')}
params = {"key": os.getenv('FILE_UPLOAD_SECRET_KEY')}

try:
    URL = "https://fillerlist.onrender.com/update/"
    # URL = "http://localhost:8000/update/"

    response = post(URL, files=files, data=params).json()

    if response["status"] == "ok":
        print("File uploaded successfully")
        exit(0)

    raise Exception("File upload failed")

except Exception as e:
    print(e)
    print("Some error occurred")
    exit(1)

