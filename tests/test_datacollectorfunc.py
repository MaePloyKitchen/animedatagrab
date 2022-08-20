from animedatagrablib import datacollectorfuncs

def test_basic_pull_count():
    assert len(datacollectorfuncs.get_anime_basic("Action",1)) == 100


