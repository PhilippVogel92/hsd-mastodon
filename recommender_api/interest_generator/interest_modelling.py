from .preprocessing import TextPreprocessor
from ..model.status_queries import persist_status_interest_relation, get_status_by_id
from ..model.interest_queries import get_all_interests_with_name_and_id, set_last_status_at
from langdetect import detect
import time
from flask import abort


class InterestGenerator:
    """Class to extract keywords from a text and compare them with interests."""

    def __init__(self, status_id, nlp_model_loader, threshold=0.6):
        self.nlp_model_loader = nlp_model_loader
        self.threshold = threshold
        self.status_id = status_id
        self.status = ""
        self.nlp = ""

    def choose_nlp_model(self, status):
        """Function to choose the right NLP model."""
        language = detect(status["text"])
        nlp_model = "de_core_news_lg"
        if language == "en":
            nlp_model = "en_core_web_lg"

        nlp = self.nlp_model_loader.get_model(nlp_model)
        return nlp

    def extract_keywords(self, text):
        """Function to extract keywords from a text."""
        doc = self.nlp(text)
        keywords = []

        # Extract keywords from text
        for token in doc:
            if token.pos_ in ["VERB", "NOUN", "PROPN"]:
                if token.text not in keywords:
                    keywords.append(token.text.lower())

        return keywords

    def match_interests_with_status(self, interests):
        """
        Function to match interests with text.
        Params: interests: List of interests from database.
        Return: List of interests which match with the text.
        """
        persisted_relations = []
        status_text = self.status["preprocessed_content"]
        status_id = self.status["id"]
        keywords = self.extract_keywords(status_text)
        matches = []

        start_time = time.time()
        max_duration = 29  # Setze die maximale Dauer auf 50 Sekunden

        for keyword_doc in self.nlp.pipe(keywords):
            for interest_doc, interest_id in self.nlp.pipe(interests, as_tuples=True):
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

    def generate_interests(self):
        """Function to generate interests for a status."""
        try:
            self.status = get_status_by_id(self.status_id)
            interests = get_all_interests_with_name_and_id()
        except IndexError:
            abort(404)

        with open("log_interests_modelling.txt", "a") as f:
            print("Triggered interest modelling for status:", self.status["id"], file=f)

        start = time.time()

        # initialize text preprocessor
        self.nlp = self.choose_nlp_model(self.status)
        nlp_model_name = self.nlp.meta["lang"] + "_" + self.nlp.meta["name"]
        text_preprocessor = TextPreprocessor(self.nlp_model_loader, nlp_model_name)
        self.status["preprocessed_content"] = text_preprocessor.sentence_preprocessing(self.status["text"])

        # extract keywords from text
        matches = self.match_interests_with_status(interests)

        end = time.time()
        diff = end - start

        # safe all print statements in a file
        with open("log_interests_modelling.txt", "a") as f:
            print(
                "Zeitaufwand:",
                diff,
                "/ NLP Modell:",
                nlp_model_name,
                "/ Status:",
                self.status["text"],
                "/ Preprocessed Text:",
                self.status["preprocessed_content"],
                "/ Matches:",
                matches,
                file=f,
            )
        return matches
