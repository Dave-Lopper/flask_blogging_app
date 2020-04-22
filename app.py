from flask import Blueprint, Flask


app = Flask(__name__)

home_bp = Blueprint('home', __name__)

@home_bp.route('/', defaults={'name': 'Dave Lopper'})
@home_bp.route('/<name>')
def home(name):
    return f"Hello {name} !"

app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run()