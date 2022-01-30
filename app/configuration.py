from app import app, render_template, request
import json


with open('app/settings.json', 'r') as settings_file:
    settings = json.loads(settings_file.read())


@app.route('/configuration.html')
def config():
    return render_template('configuration.html', settings=settings)
