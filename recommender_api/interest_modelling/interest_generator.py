from .preprocessing import TextPreprocessor
from ..model.status_queries import persist_status_interest_relation, get_status_by_id
from ..model.interest_queries import get_all_interests_with_name_and_id, set_last_status_at
from langdetect import detect
import time
from flask import abort


class InterestGenerator:
    """Class to extract keywords from a text and compare them with interests."""

    def __init__(self, nlp_model_loader, threshold=0.6):
        self.nlp_model_loader = nlp_model_loader
        self.threshold = threshold

    def choose_nlp_model(self, status):
        """Function to choose the right NLP model."""
        language = detect(status["text"])
        nlp_model_name = "de_core_news_lg"
        if language == "en":
            nlp_model_name = "en_core_web_lg"

        nlp_model = self.nlp_model_loader.get_model(nlp_model_name)
        return nlp_model

    def extract_keywords(self, text, nlp_model):
        """Function to extract keywords from a text."""
        doc = nlp_model(text)
        keywords = []

        # Extract keywords from text
        for token in doc:
            if token.pos_ in ["VERB", "NOUN", "PROPN"]:
                if token.text not in keywords:
                    keywords.append(token.text.lower())

        return keywords

    def match_interests_with_status(self, interests, status, nlp_model):
        """
        Function to match interests with text.
        Params: interests: List of interests from database.
        Return: List of interests which match with the text.
        """
        persisted_relations = []
        status_text = status["preprocessed_content"]
        status_id = status["id"]
        keywords = self.extract_keywords(status_text, nlp_model)
        matches = []

        start_time = time.time()
        max_duration = 29  # Setze die maximale Dauer auf 50 Sekunden

        for keyword_doc in nlp_model.pipe(keywords):
            for interest_doc, interest_id in nlp_model.pipe(interests, as_tuples=True):
                # Überprüfe, ob die maximale Dauer überschritten wurde
                if time.time() - start_time > max_duration:
                    break
                similarity = keyword_doc.similarity(interest_doc)
                if similarity >= self.threshold:
                    matches.append((interest_doc.text, keyword_doc.text, similarity, interest_id))
            else:
                continue
            break

        # Sort matches by similarity in descending order and keep only the top 3
        matches.sort(key=lambda x: x[2], reverse=True)
        top_3_matches = matches[:3]

        # Persist the top 3 matches
        for match in top_3_matches:
            interest_id = match[3]
            if (status_id, interest_id) not in persisted_relations:
                persist_status_interest_relation(status_id, interest_id)
                set_last_status_at(interest_id)
                persisted_relations.append((status_id, interest_id))

        return top_3_matches

    def generate_interests(self, status_id):
        """Function to generate interests for a status."""
        try:
            status = get_status_by_id(status_id)
            interests = get_all_interests_with_name_and_id()
        except IndexError:
            abort(404)

        with open("log_interests_modelling.txt", "a") as f:
            print("Triggered interest modelling for status:", status["id"], file=f)

        start = time.time()

        # initialize text preprocessor
        nlp_model = self.choose_nlp_model(status)
        text_preprocessor = TextPreprocessor(nlp_model)
        status["preprocessed_content"] = text_preprocessor.sentence_preprocessing(status["text"])

        # extract keywords from text
        matches = self.match_interests_with_status(interests, status, nlp_model)

        end = time.time()
        diff = end - start

        # safe all print statements in a file
        with open("log_interests_modelling.txt", "a") as f:
            print(
                "Zeitaufwand:",
                diff,
                "/ NLP Modell:",
                nlp_model.meta["lang"] + "_" + nlp_model.meta["name"],
                "/ Status:",
                status["text"],
                "/ Preprocessed Text:",
                status["preprocessed_content"],
                "/ Matches:",
                matches,
                file=f,
            )
        return matches
