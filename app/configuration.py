from app import app, render_template, request
import json


@app.route('/configuration.html', methods=['GET', 'POST'])
def config():

    with open('app/settings.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())

    if request.method == 'POST':

        tmdb_lang = request.form['tmdb_lang']
        qb_ip = request.form['qb_ip']
        qb_port = request.form['qb_port']
        qb_pass = request.form['qb_password']
        qb_username = request.form['qb_username']
        torrent_filepath = request.form['file_path']
        tmdb_api_key = request.form['tmdb_api_key']

        # Dirty way to make it work when restrictive is off
        try:
            is_restrictive_search = request.form['restrictive']
        except KeyError:
            is_restrictive_search = "off"

        new_settings = {
            "tmdb_language": tmdb_lang,
            "tmdb_api_key": tmdb_api_key,
            "qbittorrent_webui": {
                "ip": qb_ip,
                "port": qb_port,
                "credentials": {
                    "username": qb_username,
                    "password": qb_pass
                }
            },
            "default_saving_path": torrent_filepath,
            "strict_search": is_restrictive_search
        }

        with open('app/settings.json', 'w') as settings_file:
            settings_file.write(json.dumps(new_settings, indent=4))

        return render_template('configuration.html', settings=new_settings)
    else:
        return render_template('configuration.html', settings=settings)
