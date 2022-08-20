from bs4 import BeautifulSoup
import requests
import json

# import time


def link_build_basic(genre, page):

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

def link_build_advanced(url,token):
    new_link = url + f"\{token}"
    return new_link

def get_anime_basic(genre, page):
    results = []
    webpage = requests.get(link_build_basic(genre, page))
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
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    data = [spaceit.text for spaceit in soup.find(class_="borderClass").find_all(class_="spaceit_pad")]
    cleaned_up_data = [point.replace("\n","").split(":")[1].strip() for point in data]
    cleaned_up_columns = [point.replace("\n","").split(":")[0] for point in data]
    mapped_data = dict(zip(cleaned_up_columns,cleaned_up_data))
    mapped_data["Score"] = mapped_data["Score"].split(" ")[0]
    mapped_data["Popularity"] = mapped_data["Popularity"].replace("#","")
    mapped_data["Ranked"] = mapped_data["Ranked"].split("22 ")[0].replace("#","")

    if "Theme" in mapped_data:
            mapped_data["Theme"] = ",".join([theme[:len(theme)//2] for theme in mapped_data["Theme"].replace(" ","").split(",")])
    elif "Themes" in mapped_data:
        mapped_data["Themes"] = ",".join([theme[:len(theme)//2] for theme in mapped_data["Themes"].replace(" ","").split(",")])
    
    if "Genres" in mapped_data:
        mapped_data["Genres"] = ",".join([genre[:len(genre)//2] for genre in mapped_data["Genres"].replace(" ","").split(",")])
    elif "Genre" in mapped_data:
        mapped_data["Genre"] = ",".join([genre[:len(genre)//2] for genre in mapped_data["Genre"].replace(" ","").split(",")])

    if "Demographic" in mapped_data:
        mapped_data["Demographic"] = ",".join([demo[:len(demo)//2] for demo in mapped_data["Demographic"].replace(" ","").split(",")])
    
    mapped_data["Producers"] = ",".join([producer.strip() for producer in mapped_data["Producers"].split(",")])
    if not len(mapped_data["Aired"].split("to")) < 2:
        air_start = mapped_data["Aired"].split("to")[0].strip()
        air_finish = mapped_data["Aired"].split("to")[1].strip()
        mapped_data.pop("Aired")
        mapped_data["Air_Start"] = air_start
        mapped_data["Air_Finish"] = air_finish
    return mapped_data

def get_anime_stats(url):
    link = link_build_advanced(url,"stats")
    webpage = requests.get(link)
    soup = BeautifulSoup(webpage.content, "html.parser")
    

    

def get_anime_characters(url):
    link_build_advanced(url,"characters")
