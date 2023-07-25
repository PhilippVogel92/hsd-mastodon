import os

from dotenv import load_dotenv
from flask import Flask

from recommender_api.routes.recommender_route import recommender_route

load_dotenv()

app = Flask(__name__)
app.register_blueprint(recommender_route)
if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
