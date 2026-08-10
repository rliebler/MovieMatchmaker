import os
import requests
from dotenv import load_dotenv

load_dotenv("../.env")

bearer_token = os.getenv("TMDB_BEARER_TOKEN")

headers = {
    "Authorization": f"Bearer {bearer_token}",
    "accept": "application/json"
}

url = "https://api.themoviedb.org/3/genre/movie/list"

response = requests.get(url, headers=headers)

data = response.json()

# Create empty dictionary
genres = {}

# Add each genre and ID to dictionary
for genre in data["genres"]:
    genres[genre["name"]] = genre["id"]

print(genres)

# Save dictionary to genres.py
with open("genres.py", "w") as file:
    file.write("GENRES = ")
    file.write(repr(genres))