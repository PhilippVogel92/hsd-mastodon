import pandas as pd
from .preprocessing import TextPreprocessor
from ..model.mastodon_data_db import get_tags_by_toot_id, get_all_tags, persist_status_tag_relation

class KeywordExtractor:
    """Class to extract keywords from a text and compare them with hashtags."""
    def __init__(self, toot, nlp_model_loader, treshold=0.5):
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

    def extract_keywords(self, text):
        """Function to extract keywords from a text."""
        doc = self.nlp(text)

        keywords = []

        # Extract keywords from text
        for token in doc:
            if token.pos_ in ["VERB", "NOUN", "PROPN"]:
                if token.text not in keywords:
                    keywords.append(token.text)

        return keywords

    def match_hashtags_with_toot(self, hashtags):
        """Function to match hashtags with text."""
        matches = []
        toot_text = self.toot["preprocessed_content"]
        toot_id = self.toot["id"]
        keywords = self.extract_keywords(toot_text)
    
        print("Input Text:", toot_text, "Keywords found:", keywords)
        for keyword in keywords:
            keyword_doc = self.nlp(keyword.lower())

            for hashtag in hashtags:
                hashtag_id = hashtag[0]
                hashtag_name = hashtag[1]
                hashtag_doc = self.nlp(hashtag_name.lower())

                similarity = keyword_doc.similarity(hashtag_doc)

                print("Schlagwort:", keyword, "  Hashtag:", hashtag_name, "  Ähnlichkeit:", similarity)

                if similarity >= self.treshold:
                    if hashtag_name not in matches:
                        matches.append(hashtag_name)
                        persist_status_tag_relation(toot_id, hashtag_id)

        return matches

    def generate_hashtags(self):
        """Function to generate hashtags for a toot."""   
    
        # replace list with hashtags from database
        hashtags = get_all_tags()

        toot_tags = get_tags_by_toot_id(self.toot["id"])

        hashtags = [hashtag for hashtag in hashtags if hashtag[0] not in toot_tags]

        # initialize text preprocessor
        nlp_model_name = self.nlp.meta["lang"] + "_" + self.nlp.meta["name"]
        text_preprocessor = TextPreprocessor(self.nlp_model_loader, nlp_model_name)

        # preprocess text and clean it from html tags, urls, newlines, etc.
        self.toot["preprocessed_content"] = text_preprocessor.sentence_preprocessing(self.toot["text"])
        print("Text:", self.toot["preprocessed_content"])

        # extract keywords from text
        tags = self.match_hashtags_with_toot(hashtags)
        print("Tags:", tags)

        # add hashtags to toot
        self.toot["tags"] = tags

        return self.toot
