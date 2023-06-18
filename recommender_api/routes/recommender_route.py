from flask import Blueprint, jsonify, request
from recommender_api.utils.tfidf import recommend_with_tfidf
from flask_cors import cross_origin
recommender_route = Blueprint('recommender_route', __name__)

@recommender_route.route('/recommend-tfidf', methods=['POST'])
@cross_origin()
def get_recommendations():
    user_input = request.get_json()
    recommendations = recommend_with_tfidf(user_input['sentence'], user_input['number_of_recommendations'])
    return jsonify(recommendations)
