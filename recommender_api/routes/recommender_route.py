from flask import Blueprint, jsonify, request

from recommender_api.utils.tfidf_demo import (
    recommend_with_tfidf_for_account,
)

from recommender_api.utils.ranking_system import get_recommendations_with_ranking_system

recommender_route = Blueprint("recommender_route", __name__)


@recommender_route.route("/recommend-tfidf/account", methods=["POST"])
# @cross_origin()
def get_account_recommendations():
    user_input = request.get_json()
    recommendations = recommend_with_tfidf_for_account(
        user_input["account_id"], user_input["number_of_recommendations"]
    )
    return jsonify(recommendations)


@recommender_route.route("/recommend-ranking-system", methods=["POST"])
# @cross_origin()
def get_account_recommendations_with_ranking_system():
    user_input = request.get_json()
    recommendations = get_recommendations_with_ranking_system(
        user_input["account_id"],
        user_input["number_of_recommendations"],
        user_input["similarity_concept"],
    )
    return jsonify(recommendations)
