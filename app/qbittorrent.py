from qbittorrent import Client
import json

class Searcher:

    """ Class to add features to original qBittorrent library """


    def __init__(self, username, password, url) -> None:
        self.qb = Client(url)
        self.qb.login(username, password)

    def search(self, name):
        pass

    def add_plugin(self, plugin_url):
        pass

