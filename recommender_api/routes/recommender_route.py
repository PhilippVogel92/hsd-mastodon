from flask import Blueprint, jsonify, request, abort

from recommender_api.ranking_system.ranking_system import RankingSystem
from recommender_api.interest_generator.interest_modelling import InterestGenerator
from recommender_api.interest_generator.nlp_model_loader import NLPModelLoader
from recommender_api.dto.user_input_dto import UserInputDTO

recommender_route = Blueprint("recommender_route", __name__)

ranking_system = RankingSystem()
nlp_model_loader = NLPModelLoader()
nlp_model_loader.load_model("en_core_web_lg")
nlp_model_loader.load_model("de_core_news_lg")


#@recommender_route.route("/accounts/<account_id>/recommendations", methods=["POST"]) besser GET
@recommender_route.route("/accounts/<account_id>/create-sorted-timeline", methods=["POST"])
def sort_timeline(account_id):
    user_input = request.get_json()
    try:
        dto = UserInputDTO(**user_input)
    except TypeError:
        abort(400)
    recommendations = ranking_system.sort_timeline(account_id, dto.status_ids)
    return jsonify(recommendations)


#@recommender_route.route("/statuses/<status_id>/interests", methods=["PUT"])
@recommender_route.route("/statuses/<status_id>/generate-interests", methods=["GET"])
def generate_interests_for_status(status_id):
    interest_generator = InterestGenerator(status_id, nlp_model_loader)
    matches = interest_generator.generate_interests()
    return jsonify(matches)
