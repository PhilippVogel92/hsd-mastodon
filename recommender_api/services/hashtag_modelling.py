from .preprocessing import TextPreprocessor
from ..model.status_queries import persist_status_tag_relation
from ..model.tag_queries import get_all_tags_with_name_and_id, get_tags_by_status_id
from langdetect import detect
import time


class TagGenerator:
    """Class to extract keywords from a text and compare them with hashtags."""

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
        # print nlp model name in log file
        with open("log_hashtag_modelling.txt", "a") as f:
            print(
                "NLP Model:",
                self.nlp.meta["lang"] + "_" + self.nlp.meta["name"],
                doc.text,
                [(token.text, token.pos_) for token in doc],
                file=f,
            )

        return keywords

    def match_hashtags_with_status(self, hashtags):
        """Function to match hashtags with text."""
        matches = []
        status_text = self.status["preprocessed_content"]
        status_id = self.status["id"]
        keywords = self.extract_keywords(status_text)
        print("Input Text:", status_text, "Keywords found:", keywords)

        for keyword_doc in self.nlp.pipe(keywords):
            for hashtag_doc, hashtag_id in self.nlp.pipe(hashtags, batch_size = 500, as_tuples=True):
                hashtag_name = hashtag_doc.text
                similarity = keyword_doc.similarity(hashtag_doc)
                if similarity >= self.treshold:
                    if hashtag_name not in matches:
                        matches.append(hashtag_name)
                        persist_status_tag_relation(status_id, hashtag_id)
        return matches

    def generate_hashtags(self):
        """Function to generate hashtags for a status."""

        # timer which stops the second from start to end
        start = time.time()

        # get all hashtags from database
        hashtags = get_all_tags_with_name_and_id()

        status_tags = get_tags_by_status_id(self.status["id"])

        hashtags = [hashtag for hashtag in hashtags if hashtag[0] not in status_tags]

        # initialize text preprocessor
        nlp_model_name = self.nlp.meta["lang"] + "_" + self.nlp.meta["name"]
        text_preprocessor = TextPreprocessor(self.nlp_model_loader, nlp_model_name)

        # preprocess text and clean it from html tags, urls, newlines, etc.
        self.status["preprocessed_content"] = text_preprocessor.sentence_preprocessing(self.status["text"])
        print("Text:", self.status["preprocessed_content"])

        # extract keywords from text
        tags = self.match_hashtags_with_status(hashtags)

        # add hashtags to status
        self.status["tags"] = tags

        end = time.time()
        diff = end - start
        print(
            "------------Zeitaufwand:",
            diff,
            "für Status:",
            self.status["text"],
            ". Gefundene Tags:",
            self.status["tags"],
            "-----------------",
        )
        # safe all print statements in a file
        with open("log_hashtag_modelling.txt", "a") as f:
            print(
                "Zeitaufwand:",
                diff,
                "/ Status:",
                self.status["text"],
                "/ Preprocessed Text:",
                self.status["preprocessed_content"],
                "/ Keywords:",
                self.extract_keywords(self.status["preprocessed_content"]),
                "/ Gefundene Tags:",
                self.status["tags"],
                "-----------------",
                file=f,
            )

        return self.status["tags"]
