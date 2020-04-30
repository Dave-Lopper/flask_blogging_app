# /manage.py
from dotenv import load_dotenv

from app.boot import create_app
from app.blueprints import main

load_dotenv(".env")

app = create_app()
app.register_blueprint(main)

if __name__ == "__main__":
    app.run()
