import os

from dotenv import load_dotenv
from flask import Flask
from .utils.interests_data import get_google_trends


# from flask_cors import CORS, cross_origin
from recommender_api.routes.recommender_route import recommender_route
load_dotenv()

app = Flask(__name__)
app.register_blueprint(recommender_route)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
if __name__ == '__main__':
    get_google_trends()
    app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
