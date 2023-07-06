from flask import Blueprint, jsonify, request
from ..model.status_queries import get_status_by_id

from recommender_api.services.ranking_system import RankingSystem
from recommender_api.services.hashtag_modelling import TagGenerator
from recommender_api.services.nlp_model_loader import NLPModelLoader

recommender_route = Blueprint("recommender_route", __name__)

nlp_model_loader = NLPModelLoader()
nlp_model_loader.load_model("en_core_web_lg")
nlp_model_loader.load_model("de_core_news_lg")

ranking_system = RankingSystem()


@recommender_route.route("/accounts/<account_id>/create-sorted-timeline", methods=["POST"])
def sort_timeline(account_id):
    user_input = request.get_json()
    recommendations = ranking_system.sort_timeline(
        account_id,
        user_input["status_ids"],
    )
    return jsonify(recommendations)


@recommender_route.route("/statuses/<status_id>/generate-tags", methods=["POST"])
def generate_tag_for_status(status_id):
    status = get_status_by_id(status_id)
    tag_generator = TagGenerator(status, nlp_model_loader)
    status_with_tag = tag_generator.generate_hashtags()
    return jsonify(status_with_tag)
