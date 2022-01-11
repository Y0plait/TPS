import logging
from flask import Flask, render_template
from flask import request

import BackEnd.searcher

app = Flask(__name__)
logging.basicConfig(filename='./flask_app.log', filemode='w',
                    format='%(asctime)s ; %(levelname)s: %(message)s', level=logging.WARNING)


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
        worker = BackEnd.searcher.TorrentSearcher(movie, lang, quality)
        data = worker._get_magnet_links()

        return render_template('search.html', result=data, quality=quality, data=data)

    except Exception as e:
        data = dict()
        quality = str()
        logging.warn(f'Error occured: {e}')
        return render_template('search.html', result=data, quality=quality, data=data)
