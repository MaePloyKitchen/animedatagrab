from bs4 import BeautifulSoup
import requests

webpage = requests.get("https://myanimelist.net/anime/genre/1/Action?page=3")

soup = BeautifulSoup(webpage.content,'html.parser')

containers = soup.find_all(class_ = 'js-anime-category-producer')

print(len)

"""
Members to scrape
js-genre
info
js-score
js-members
js-startdate
""" 

for container in containers:
    print(container.find_all(class_='h2_anime_title')[0].string)
    genre_list = container.find_all(class_='genre')
    for genre in genre_list:
        print(genre.find('a').string)
    print(container.find_all(class_='js-score')[0].string)
    print(container.find_all(class_='js-members')[0].string)

