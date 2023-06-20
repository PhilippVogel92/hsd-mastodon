import spacy
import pandas as pd
from .preprocessing import TextPreprocessor


class KeywordExtractor:
    """Class to extract keywords from a text and compare them with hashtags."""

    def __init__(self, toot, nlp_model_loader, treshold=0.7):
        self.nlp_model_loader = nlp_model_loader
        self.nlp = self.choose_nlp_model(toot)
        self.treshold = treshold
        self.toot = toot

    def choose_nlp_model(self, toot):
        """Function to choose the right NLP model."""
        language = toot["language"]
        nlp_model = "de_core_news_lg"
        if language == "en":
            nlp_model = "en_core_web_lg"
            print("English language detected.")

        nlp = self.nlp_model_loader.get_model(nlp_model)
        print("Loaded NLP model:", nlp.meta["lang"] + "_" + nlp.meta["name"])
        return nlp

    def has_hashtag(self, toot):
        """Function to check if a toot contains hashtags."""
        return len(toot["tags"]) != 0

    def extract_keywords(self, text):
        """Function to extract keywords from a text."""
        doc = self.nlp(text)

        # Extract keywords from text
        keywords = [token.text for token in doc if token.pos_ in ["VERB", "NOUN", "PROPN"]]

        return keywords

    def match_hashtags_with_text(self, hashtags, text):
        """Function to match hashtags with text."""
        matches = []
        keywords = self.extract_keywords(text)

        print(text, keywords, hashtags)
        for keyword in keywords:
            keyword_doc = self.nlp(keyword.lower())

            for hashtag in hashtags:
                hashtag_doc = self.nlp(hashtag.lower())

                similarity = keyword_doc.similarity(hashtag_doc)

                print("Schlagwort:", keyword, "Hashtag:", hashtag, "Ähnlichkeit:", similarity)

                if similarity >= self.treshold:
                    matches.append(hashtag)

        return matches

    def generate_hashtags(self):
        # replace list with hashtags from database
        hashtags = [
            "Mittelaltermarkt",
            "Sport",
            "Essen",
            "Mensa",
            "Ritter",
            "Bier",
            "Kochen",
            "Kunst",
            "Kultur",
            "Musik",
            "Datascience",
            "Coding",
            "studieren",
            "Development",
        ]

        print("Has hashtag:", self.has_hashtag(self.toot))

        # return toot if it already has hashtags
        if self.has_hashtag(self.toot):
            return self.toot

        # initialize text preprocessor
        nlp_model_name = self.nlp.meta["lang"] + "_" + self.nlp.meta["name"]
        text_preprocessor = TextPreprocessor(self.nlp_model_loader, nlp_model_name)

        # preprocess text and clean it from html tags, urls, newlines, etc.
        text = text_preprocessor.sentence_preprocessing(self.toot["content"])
        print("Text:", text)

        # extract keywords from text
        tags = self.match_hashtags_with_text(hashtags, text)
        print("Tags:", tags)

        # add hashtags to toot
        self.toot["tags"] = tags

        return self.toot
