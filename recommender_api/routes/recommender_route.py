from flask import Blueprint, jsonify, request
from ..model.status_queries import get_status_by_id

from recommender_api.utils.tfidf_demo import (
    recommend_with_tfidf_for_account,
)

from recommender_api.utils.ranking_system import RankingSystem
from recommender_api.utils.hashtag_modelling import TagGenerator
from recommender_api.utils.nlp_model_loader import NLPModelLoader
from recommender_api.utils.preprocessing import TextPreprocessor

recommender_route = Blueprint("recommender_route", __name__)

nlp_model_loader = NLPModelLoader()
nlp_model_loader.load_model("en_core_web_lg")
nlp_model_loader.load_model("de_core_news_lg")

ranking_system = RankingSystem()


@recommender_route.route("/recommend-tfidf/account", methods=["POST"])
# @cross_origin()
def get_account_recommendations():
    user_input = request.get_json()
    recommendations = recommend_with_tfidf_for_account(
        user_input["account_id"],
        nlp_model_loader,
        user_input["number_of_recommendations"],
    )
    return jsonify(recommendations)


@recommender_route.route("/create-sorted-timeline", methods=["POST"])
# @cross_origin()
def sort_timeline():
    user_input = request.get_json()
    recommendations = ranking_system.sort_timeline(
        user_input["account_id"],
        user_input["status_ids"],
        nlp_model_loader,
        user_input["number_of_recommendations"],
    )
    return jsonify(recommendations)


@recommender_route.route("/statuses/<status_id>/generate-tags", methods=["POST"])
# @cross_origin()
def generate_tag_for_status(status_id):
    status = get_status_by_id(status_id)
    tag_generator = TagGenerator(status, nlp_model_loader)
    status_with_tag = tag_generator.generate_hashtags()
    return jsonify(status_with_tag)


# überarbeiten REST konform!!!
@recommender_route.route("/preprocess-status", methods=["POST"])
# @cross_origin()
def preprocess_status():
    user_input = request.get_json()
    text_preprocessor = TextPreprocessor(nlp_model_loader, user_input["status"])
    preprocessed_status = text_preprocessor.status_preprocessing()
    return jsonify(preprocessed_status)
