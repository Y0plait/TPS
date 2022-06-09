from tmdbv3api import Movie, TMDb


try:
    from utils import update_tmdb_database
except ModuleNotFoundError or ImportError:
    from sys import path
    path.insert(1, './app/')
    from utils import update_tmdb_database

from app import app, redirect, render_template, request, url_for


"""
@app.before_request
def before_request():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print(ip, request.url)


@app.after_request
def after_request(response):
    return response
"""

popular_films = update_tmdb_database()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():

    # User searched a movie:
    if request.method == 'POST':
        searched_movie = request.form['search-name']
        if searched_movie == "":
            return render_template('index.html', data=popular_films, error="Please enter a movie name")
        else:
            # Redirects to the search results function
            return redirect(url_for("search_results", search=searched_movie))

    # User access the page
    else:
        return render_template('index.html', data=popular_films, error="")


# When a poster on the index.html is clicked call this function :
@app.route('/movie/<mov_id>', methods=['GET', 'POST'])
def mov_details(mov_id):

    movie = Movie()
    m = movie.details(mov_id)
    # User clicks the download button:
    print(m.title)
    if request.method == 'POST':
        # TODO make call to download-torrent.py when button clicked
        return render_template('details.html', movie_data=m, id=mov_id)

    # User access the page
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
