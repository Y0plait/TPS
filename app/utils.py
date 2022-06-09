import json
from tmdbv3api import Movie, TMDb
from datetime import date
from pathlib import Path


def update_tmdb_database():
    """
    Update the trending movies from TMDb
    """
    # Loading the configuration file:
    conf = load_config()

    tmdb = TMDb()
    tmdb.api_key = conf['tmdb_api_key']
    tmdb_poster_url = 'https://www.themoviedb.org/t/p/w400'

    tmdb.language = conf['tmdb_language']
    tmdb.debug = True

    popular_today_file = f'app/tmdb/{date.today()}.json'
    path = Path(popular_today_file)
    if path.is_file():
        with open(popular_today_file, 'r', encoding='utf-8') as pop_file:
            popular_films = json.loads(pop_file.read())

    else:
        movie = Movie()
        popular = movie.popular()
        formatted_pop = {}

        for p in popular:
            formatted_pop.update({
                p.id: {
                    'title': p.title,
                    'poster_path': tmdb_poster_url + p.poster_path,
                }
            })

        with open(popular_today_file, 'w', encoding='utf-8') as pop_file:
            pop_file.write(json.dumps(formatted_pop, indent=4))

        popular_films = formatted_pop

    return popular_films


def load_config():
    """
    Load configuration file located in app/settings.json
    """
    with open('app/settings.json', 'r') as conf_file:
        return json.loads(conf_file.read())
