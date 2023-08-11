import os

from dotenv import load_dotenv
from flask import Flask

from recommender_api.routes.recommender_route import blueprint

load_dotenv()

app = Flask(__name__)
app.register_blueprint(blueprint)
if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
