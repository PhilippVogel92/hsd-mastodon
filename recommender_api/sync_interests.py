from .model.tag_queries import get_all_tags_with_name_and_id
from .model.interest_queries import persist_interest
from recommender_api.services.nlp_model_loader import NLPModelLoader

nlp_model_loader = NLPModelLoader()
nlp_model_loader.load_model("en_core_web_lg")
nlp_model_loader.load_model("de_core_news_lg")

tags = get_all_tags_with_name_and_id()

count = 0
for tag in tags:
    enToken = nlp_model_loader.get_model("en_core_web_lg")(tag[0])
    deToken = nlp_model_loader.get_model("de_core_news_lg")(tag[0])
    if enToken.has_vector or deToken.has_vector:
      persist_interest(tag[0])





