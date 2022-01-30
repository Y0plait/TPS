from app import app

try:
    if __name__ == '__main__':
        app.run(debug=True, host="0.0.0.0")
except Exception:
    pass
