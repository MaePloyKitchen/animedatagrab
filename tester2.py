import animesuggestor
import json
import os

os.chdir("DataFiles")

#Generates a bunch of basic files

genres = [
    "Action",
    "Adventure",
    "Avant_Garde",
    "Award_Winning",
    "Boys_Love",
    "Comedy",
    "Drama",
    "Fantasy",
    "Girls_Love",
    "Gourmet",
    "Horror",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Slice_of_Life",
    "Sports",
]

for genre in genres:
    results = animesuggestor.get_anime_basic(genre,2)
    with open(f"animedatagrab_{genre}.json","w") as infile:
        json.dump(results,infile)