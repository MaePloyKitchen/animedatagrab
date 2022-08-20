import animesuggestor
import json
import os

#Takes in basic file and turns it into advanced data.

os.chdir("DataFiles")

genre = "Sports"

with open(f"animedatagrab_{genre}.json","r") as outfile:
    animes = json.load(outfile)
    links = [anime["Link"] for anime in animes]


results = []
for link in links:
    anime = animesuggestor.get_anime_advanced(link)
    results.append(anime)

with open(f"anime{genre}Advanced.json","w") as infile:
    json.dump(results, infile)

