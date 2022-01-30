from app import app, render_template, request, redirect, url_for
from tmdbv3api import TMDb, Movie
from datetime import date
from pathlib import Path
import json

tmdb = TMDb()
tmdb.api_key = '0b8f04cc00bf9b715120f6d1667612e7'
tmdb_poster_url = 'https://www.themoviedb.org/t/p/w400'

tmdb.language = 'fr'
tmdb.debug = True

popular_today_file = f'./app/tmdb/{date.today()}.json'
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        searched_movie = request.form['search-name']
        if searched_movie == "":
            return render_template('index.html', data=popular_films, error="Please enter a movie name")
        else:
            return redirect(url_for("search_results", search=searched_movie))
    else:
        return render_template('index.html', data=popular_films, error="")

# When a poster on the index.html is clicked call this function :


@app.route('/movie/<mov_id>', methods=['GET', 'POST'])
def mov_details(mov_id):

    movie = Movie()
    m = movie.details(mov_id)

    if request.method == 'POST':

        return render_template('details.html', movie_data=m, id=mov_id)
    else:
        return render_template('details.html', movie_data=m, id=mov_id)


# Function called when something is searched on the searchbar of the index
@app.route('/results?<search>', methods=['GET', 'POST'])
def search_results(search):

    if request == "POST":
        return redirect(url_for('index'))
    else:
        initial_search = search
        movie = Movie()
        search = movie.search(initial_search)
        form_search = {}
        for s in search:
            form_search.update({
                s.id: s
            })

        return render_template("results.html", data=form_search, search=initial_search)
