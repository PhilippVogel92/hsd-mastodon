import json
from flask import Flask
from flask import request
#from flask_cors import CORS, cross_origin
from recommender_api.routes.recommender_route import recommender_route

app = Flask(__name__)
app.register_blueprint(recommender_route)
#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'
if __name__ == '__main__':
    app.run(port=8080)
