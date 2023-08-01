from recommender_api.ranking_system.ranking_system import RankingSystem 
from recommender_api.dto.user_input_dto import UserInputDTO
from flask import jsonify, request, abort

ranking_system = RankingSystem()

def sort_timeline(account_id):
    user_input = request.get_json()
    try:
        dto = UserInputDTO(**user_input)
    except TypeError:
        abort(400)
    recommendations = ranking_system.sort_timeline(account_id, dto.status_ids)
    return jsonify(recommendations)
