from qbittorrent import Client
from utils import load_config
from requests.exceptions import HTTPError

fr_abbr = ['vostfr', 'VOSTFR', 'fr', 'FR', 'truefrench', 'Truefrench']
conf = load_config()

search_plugins = [
    "https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/thepiratebay.py",
    "https://raw.githubusercontent.com/MaurizioRicci/qBittorrent_search_engines/master/cpasbien.py",
    "https://raw.githubusercontent.com/nindogo/qbtSearchScripts/master/magnetdl.py"
]

qb = Client(conf["qbittorrent_webui"]["ip"]
            + ":"
            + conf["qbittorrent_webui"]["port"])

qb.login(conf["qbittorrent_webui"]["credentials"]["username"],
         conf["qbittorrent_webui"]["credentials"]["password"])


def check_plugins():
    if qb.list_search_plugins() is []:
        qb.add_search_plugin(search_plugins)
    else:
        pass


def search(name):
    check_plugins()
    try:
        movie_search = qb.search(name)
    except HTTPError:
        qb.login(conf["qbittorrent_webui"]["credentials"]["username"],
                 conf["qbittorrent_webui"]["credentials"]["password"])
        movie_search = qb.search(name)

    finally:
        if "No results returned" in str(movie_search) or movie_search['total'] is 1:
            raise Exception("No movie were found.")
        else:
            pass

    return
