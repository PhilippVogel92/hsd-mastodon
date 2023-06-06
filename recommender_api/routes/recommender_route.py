from flask import Blueprint, jsonify, request
from recommender_api.services.recommender import recommend
from recommender_api.services.recommender_tfidf import recommend_tfidf

recommender_route = Blueprint('recommender_route', __name__)

@recommender_route.route('/recommend', methods=['POST'])
#@cross_origin()
def get_recommendations():
    user_input = request.get_json()
    recommendations = recommend(user_input['dataset'], user_input['number_of_recommendations'], user_input['user'])
    return jsonify(recommendations)

#old route
@recommender_route.route('/recommend-tfidf', methods=['POST'])
#@cross_origin()
def get_recommendations_tfidf():
    user_input = request.get_json()
    recommendations = recommend_tfidf(user_input['sentence'], user_input['number_of_recommendations'])
    return jsonify(recommendations)