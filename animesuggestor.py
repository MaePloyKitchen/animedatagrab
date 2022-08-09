from bs4 import BeautifulSoup
import requests
import json

# import time


def link_build(genre, page):

    id_genre_mapping = {
        "Action": 1,
        "Adventure": 2,
        "Avant_Garde": 5,
        "Award_Winning": 46,
        "Boys_Love": 28,
        "Comedy": 4,
        "Drama": 8,
        "Fantasy": 10,
        "Girls_Love": 26,
        "Gourmet": 47,
        "Horror": 14,
        "Mystery": 7,
        "Romance": 22,
        "Sci-Fi": 24,
        "Slice_of_Life": 36,
        "Sports": 30,
        "Supernatural": 37,
        "Suspense": 41,
        "Ecchi": 9,
        "Erotica": 49,
        "Hentai": 12,
    }

    link = f"https://myanimelist.net/anime/genre/{id_genre_mapping[genre]}/{genre}?page={page}"
    # webpage = requests.get(link)
    # soup = BeautifulSoup(webpage.content, "html.parser")
    # containers = soup.find_all(class_="js-anime-category-producer")
    # return contain
    return link


def get_anime_basic(genre, page):
    results = []
    webpage = requests.get(link_build(genre, page))
    soup = BeautifulSoup(webpage.content, "html.parser")
    containers = soup.find_all(class_="js-anime-category-producer")

    for container in containers:
        anime = dict()
        anime["Title"] = container.find_all(class_="js-title")[0].string
        genre_list = container.find_all(class_="genre")
        genres = [genre.find("a").string for genre in genre_list]
        anime["Genres"] = genres
        anime["Score"] = container.find_all(class_="js-score")[0].string
        anime["Members"] = container.find_all(class_="js-members")[0].string
        anime["Start_Date"] = container.find_all(class_="js-start_date")[0].string
        anime_title = container.find_all(class_="h2_anime_title")[0]
        anime["Link"] = anime_title.find_all("a", href=True)[0]["href"]
        results.append(anime)
    return results


def get_anime_advanced(url):
    results = []
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")


genre = "Adventure"
page = 1

with open(f"animedump_{genre}.json", "w") as infile:
    json.dump(get_anime_basic(genre, 1), infile)
