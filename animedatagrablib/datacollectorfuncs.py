from bs4 import BeautifulSoup
import requests
import json

# import time


def link_build_basic(genre, page,media):

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
        "Adult_Cast":50,
        "Anthropomorphic":51,
        "CGDCT":52,
        "Childcare":53,
        "Combat_Sports":54,
        "Crossdressing":81,
        "Delinquents":55,
        "Detective":39
    }

    link = f"https://myanimelist.net/{media}/genre/{id_genre_mapping[genre]}/{genre}?page={page}"
    
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
    results = dict()
    link = link_build_advanced(url,"stats")
    webpage = requests.get(link)
    soup = BeautifulSoup(webpage.content, "html.parser")
    container = soup.find_all(class_="rightside")[0]
    data = container.find_all(class_="spaceit_pad")
    view_stats_columns = [d.text.split(":")[0] for d in data[:6]]
    view_stats_data = [d.text.split(":")[1].strip() for d in data[:6]]
    mapped_view_stats = dict(zip(view_stats_columns,view_stats_data))
    results["Stats_Tab"] = mapped_view_stats
    ranking_data_percents = [d.text.split(" ")[0].replace("\xa0","") for d in data[6:]]
    ranking_data_votes = [d.text.split(" ")[1].strip("(") for d in data[6:]]
    ranking_data_columns = [num for num in range(10,0,-1)]
    mapped_data = dict()
    for ind , column in enumerate(ranking_data_columns):
        mapped_data[column] = {"Percent":ranking_data_percents[ind],"Votes":ranking_data_votes[ind]}
    results["Ranking"] = mapped_data
    return results

    

def get_anime_voice_actors(url):
    results = []
    link = link_build_advanced(url,"characters")
    webpage = requests.get(link)
    soup = BeautifulSoup(webpage.content, "html.parser")
    characters = soup.find_all(class_="js-anime-character-table")
    for character in characters:
        #Character Names
        char = dict()
        char["Name"] = character.find(class_="js-chara-roll-and-name").text.strip()
        #Number of Favorites
        char["Favorites"] = character.find(class_="js-anime-character-favorites").text.strip()
        voice_actors_container = character.find_all(class_="js-anime-character-va-lang")
        voice_actor_dict = dict()
        for ind,voice in enumerate(voice_actors_container):
            #VA one
            va = dict()
            con = voice.find(class_="spaceit_pad")
            va["Name"] = con.text.strip()
            va["Link"] = con.find("a",href=True)["href"]
            #VA Language
            va["Language"] = voice.find(class_="js-anime-character-language").text.strip()
            voice_actor_dict[f"{ind}"] = va
        char["Voice_Actors"] = voice_actor_dict
        results.append(char)
    return results


def get_manga_basic(genre, page):
    pass

def get_manga_advanced(url):
    pass