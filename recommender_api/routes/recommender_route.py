from flask import Blueprint, jsonify, request, abort
from ..model.status_queries import get_status_by_id

from recommender_api.services.ranking_system import RankingSystem
from recommender_api.services.interest_modelling import InterestGenerator
from recommender_api.services.nlp_model_loader import NLPModelLoader
from recommender_api.dto.user_input_dto import UserInputDTO

recommender_route = Blueprint("recommender_route", __name__)

nlp_model_loader = NLPModelLoader()
nlp_model_loader.load_model("en_core_web_lg")
nlp_model_loader.load_model("de_core_news_lg")

ranking_system = RankingSystem()


@recommender_route.route("/accounts/<account_id>/create-sorted-timeline", methods=["POST"])
def sort_timeline(account_id):
    user_input = request.get_json()
    print(user_input)

    try:
        dto = UserInputDTO(**user_input)
    except TypeError:
        abort(400)
    recommendations = ranking_system.sort_timeline(account_id, dto.status_ids)
    return jsonify(recommendations)



@recommender_route.route("/statuses/<status_id>/generate-interests", methods=["GET"])
def generate_interests_for_status(status_id):
    try:
        status = get_status_by_id(status_id)
    except IndexError:
        abort(404)
    interest_generator = InterestGenerator(status, nlp_model_loader)
    matches = interest_generator.generate_interests()
    return jsonify(matches)
