from flask import Blueprint, jsonify, request
from ..model.mastodon_data_db import get_status_by_id

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


@recommender_route.route("/recommend-tfidf/account", methods=["POST"])
# @cross_origin()
def get_account_recommendations():
    user_input = request.get_json()
    recommendations = recommend_with_tfidf_for_account(
        user_input["account_id"], nlp_model_loader, user_input["number_of_recommendations"]
    )
    return jsonify(recommendations)


@recommender_route.route("/recommend-ranking-system", methods=["POST"])
# @cross_origin()
def get_account_recommendations_with_ranking_system():
    user_input = request.get_json()
    ranking_system = RankingSystem(
        number_of_recommendations=user_input["number_of_recommendations"],
        similarity_concept=user_input["similarity_concept"],
        nlp_model_loader=nlp_model_loader,
    )
    recommendations = ranking_system.get_recommendations_with_ranking_system(
        user_input["account_id"],
    )
    return jsonify(recommendations)


@recommender_route.route("/statuses/<status_id>/generate-tags", methods=["POST"])
# @cross_origin()
def generate_tag_for_status(status_id):
    status = get_status_by_id(status_id)
    keyword_extractor = TagGenerator(status, nlp_model_loader)
    status_with_tag = keyword_extractor.generate_hashtags()
    return jsonify(status_with_tag)


@recommender_route.route("/preprocess-status", methods=["POST"])
# @cross_origin()
def preprocess_status():
    user_input = request.get_json()
    text_preprocessor = TextPreprocessor(nlp_model_loader, user_input["status"])
    preprocessed_status = text_preprocessor.status_preprocessing()
    return jsonify(preprocessed_status)
