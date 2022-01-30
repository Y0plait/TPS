# TPS
## _A python torrent searcher_


TPS is a python movie researcher scrapper. It scraps data from ThePirateBay and Torrent9's sites (for the moment).

- Type the name of your movie
![SearchBar](https://github.com/Y0plait/TPS/tree/master/src/static/images/SearchBar.png "")
- Click on search
- And here you go !! A list with all the results with their name, magnet link, size and even number of seeders !

## Features


- **✔** Choose the language of the movie (currently only French and English are available).
- **✔** Choose the quality of the movie.
- **(In work)** Automatically download your movie by simply clicking the little ➕ button next to its number of seeders.
- **(In work)** Export the output to a csv.

## Prerequisites:

- Python 3.X
- [qBittorrent](https://www.qbittorrent.org/ "qBittorrent")
- [qBittorrent\'s WebUI enabled](https://lgallardo.com/2014/09/29/como-activar-la-interfaz-web-de-qbittorrent/ "qBittorrent's WebUI enabled")

## How does it works ?

- #### Web GUI:

	- A [Flask](https://github.com/pallets/flask "Flask") web server 

- #### Torrent Downloading:

	- [qBitTorrent python library](https://github.com/v1k45/python-qbittorrent "qBitTorrent python library") 

- #### Scraping:

	- qBittorrent integrated search engine

## Installation

**⚠️ I higly recommend running this on a Linux-server ⚠️**

- Clone the repository :

	 ```bash 
	 $ git clone https://github.com/Y0plait/TPS.git
	 $ cd TPS
	 ```

- Install the required libraries :

	```bash
	 $ pip install -r requirements.txt
	```

- Edit the `app/settings.json` file :
	```json
	{
    "tmdb_language": "FR",
    "qbittorrent_webui": {
        "ip": "127.0.0.1",
        "port": "8080",
        "credentials": {
            "username": "admin",
            "password": "pass"
        }
    },
    "default_saving_path": "",
    "strict_search": false
}
	```

- Launch the Flask Web Server :

	```bash
	TODO
	```
