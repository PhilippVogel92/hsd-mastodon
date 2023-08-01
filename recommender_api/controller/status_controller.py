from recommender_api.interest_generator.interest_modelling import InterestGenerator
from recommender_api.interest_generator.nlp_model_loader import NLPModelLoader
from flask import jsonify

class StatusController:
    
    def __init__(self):
        self.nlp_model_loader = NLPModelLoader()
        self.nlp_model_loader.load_model("en_core_web_lg")
        self.nlp_model_loader.load_model("de_core_news_lg")
        self.interests_generator = InterestGenerator(self.nlp_model_loader)

    def generate_interests(self, status_id):
        matches = self.interests_generator.generate_interests(status_id)
        return jsonify(matches)
