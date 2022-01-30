from app import app, render_template


@app.route('/features.html')
def features():
    return render_template('features.html')
