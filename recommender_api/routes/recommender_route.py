from flask import Blueprint, jsonify, request
from recommender_api.utils.tfidf import recommend_with_tfidf, recommend_with_tfidf_for_account
recommender_route = Blueprint('recommender_route', __name__)

@recommender_route.route('/recommend-tfidf', methods=['POST'])
#@cross_origin()
def get_recommendations():
    user_input = request.get_json()
    recommendations = recommend_with_tfidf(user_input['sentence'], user_input['number_of_recommendations'])
    return jsonify(recommendations)

@recommender_route.route('/recommend-tfidf/account', methods=['POST'])
#@cross_origin()
def get_account_recommendations():
    user_input = request.get_json()
    recommendations = recommend_with_tfidf_for_account(user_input['account_id'], user_input['number_of_recommendations'])
    return jsonify(recommendations)