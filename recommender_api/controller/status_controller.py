from recommender_api.interest_generator.interest_modelling import InterestGenerator
from recommender_api.interest_generator.nlp_model_loader import NLPModelLoader
from flask import jsonify

nlp_model_loader = NLPModelLoader()
nlp_model_loader.load_model("en_core_web_lg")
nlp_model_loader.load_model("de_core_news_lg")
interests_generator = InterestGenerator(nlp_model_loader)

def generate_interests(status_id):
    matches = interests_generator.generate_interests(status_id)
    return jsonify(matches)
