from .preprocessing import TextPreprocessor
from ..model.status_queries import persist_status_interest_relation
from ..model.interest_queries import get_all_interests_with_name_and_id, get_interests_by_status_id
from langdetect import detect
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class InterestGenerator:
    """Class to extract keywords from a text and compare them with interests."""

    def __init__(self, status, nlp_model_loader, treshold=0.6):
        self.nlp_model_loader = nlp_model_loader
        self.nlp = self.choose_nlp_model(status)
        self.treshold = treshold
        self.status = status

    def choose_nlp_model(self, status):
        """Function to choose the right NLP model."""
        language = detect(status["text"])
        nlp_model = "de_core_news_lg"
        if language == "en":
            nlp_model = "en_core_web_lg"

        nlp = self.nlp_model_loader.get_model(nlp_model)
        print("Loaded NLP model:", nlp.meta["lang"] + "_" + nlp.meta["name"])
        # safe all print statements in a file
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

    """ def match_hashtags_with_status(self, hashtags):
        persisted_relations = []
        status_text = self.status["preprocessed_content"]
        status_id = self.status["id"]
        keywords = self.extract_keywords(status_text)
        matches = []
        for keyword_doc in self.nlp.pipe(keywords):
            for hashtag_doc, hashtag_id in self.nlp.pipe(hashtags, as_tuples=True):
                similarity = keyword_doc.similarity(hashtag_doc)
                if similarity >= self.treshold:
                    if (status_id, hashtag_id) not in persisted_relations:
                        persist_status_tag_relation(status_id, hashtag_id)
                        persisted_relations.append((status_id, hashtag_id, similarity))
                        matches.append((hashtag_doc.text, keyword_doc.text, similarity))

        return matches """

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
        for keyword_doc in self.nlp.pipe(keywords):
            for interest_doc, interest_id in self.nlp.pipe(interests, as_tuples=True):
                similarity = keyword_doc.similarity(interest_doc)
                if similarity >= self.treshold:
                    matches.append((interest_doc.text, keyword_doc.text, similarity, interest_id))

        # Sort matches by similarity in descending order and keep only the top 3
        matches.sort(key=lambda x: x[2], reverse=True)
        top_3_matches = matches[:3]

        # Persist the top 3 matches
        for match in top_3_matches:
            interest_id = match[3]
            if (status_id, interest_id) not in persisted_relations:
                persist_status_interest_relation(status_id, interest_id)
                persisted_relations.append((status_id, interest_id))

        return top_3_matches

    def match_hashtags_with_status_tfidf(self, hashtags):
        """
        Function to match hashtags with text and persist the relations.
        Params: hashtags: List of hashtags from database.
        """
        persisted_relations = []
        status_text = self.status["preprocessed_content"]
        status_id = self.status["id"]
        keywords = self.extract_keywords(status_text)
        matches = []

        # Compute cosine similarity between keywords and hashtags
        vectorizer = TfidfVectorizer()
        hashtag_names = [hashtag[0] for hashtag in hashtags]
        hashtag_tfidf = vectorizer.fit_transform(hashtag_names)
        keyword_tfidf = vectorizer.transform(keywords)
        similarities = cosine_similarity(keyword_tfidf, hashtag_tfidf)

        # Select hashtags with similarity above threshold
        for i, keyword in enumerate(keywords):
            for j, hashtag in enumerate(hashtags):
                similarity = similarities[i, j]
                if similarity >= self.treshold:
                    hashtag_id = hashtag[1]
                    if (status_id, hashtag_id) not in persisted_relations:
                        persist_status_interest_relation(status_id, hashtag_id)
                        persisted_relations.append((status_id, hashtag_id))
                        matches.append((hashtag[0], keyword, similarity))
        return matches

    def generate_interests(self):
        """Function to generate interests for a status."""

        # statuses from other instances should not be processed
        if not self.status["local"]:
            return "Status is not local. Interests will not be generated."

        with open("log_interests_modelling.txt", "a") as f:
            print("Triggered interest modelling for status:", self.status["id"], file=f)

        start = time.time()

        interests = get_all_interests_with_name_and_id()
        status_interests = get_interests_by_status_id(self.status["id"])
        interests = [interest for interest in interests if interest[0] not in status_interests]

        # initialize text preprocessor
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
                "/ Status:",
                self.status["text"],
                "/ Preprocessed Text:",
                self.status["preprocessed_content"],
                "/ Matches:",
                matches,
                file=f,
            )
        return matches
