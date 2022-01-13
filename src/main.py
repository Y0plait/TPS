import logging
from flask import Flask, render_template, request

import scrapper.searcher

app = Flask(__name__)
logging.basicConfig(filename='./logs/TPS.log', filemode='w',
                    format='%(asctime)s ; %(levelname)s: %(message)s', level=logging.WARNING)


# Define flask's log file to flask.log
flask_logger = logging.getLogger('werkzeug')
flask_handler = logging.FileHandler('./logs/flask.log')
flask_logger.addHandler(flask_handler)
app.logger.addHandler(flask_handler)


@app.route('/')
def index():
    try:
        return render_template('/acceuil.html')
    except Exception as e:
        return f'Ooooops something went wrong {e}'


@app.route('/info.html')
def info():
    return render_template('/info.html')


@app.route('/acceuil.html')
def acceuil():
    return render_template('/acceuil.html')


@app.route('/config.html', methods=['GET'])
def config():
    return render_template('config.html')


@app.route('/search.html', methods=['GET', 'POST'])
def search():
    try:
        movie = request.form['search-name']
        lang = request.form['lang-select']
        quality = request.form['quality-select']
        worker = scrapper.searcher.TorrentSearcher(movie, lang, quality)
        data = worker._get_magnet_links()

        return render_template('search.html', result=data, quality=quality, data=data)

    except Exception as e:
        data = dict()
        quality = str()
        logging.warn(f'Error occured: {e}')
        return render_template('search.html', result=data, quality=quality, data=data)
