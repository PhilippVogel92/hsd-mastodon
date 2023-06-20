import spacy
import re
import html2text


class TextPreprocessor:
    """Class to preprocess text data."""

    def __init__(self, nlp_model_loader, nlp_model="de_core_news_lg"):
        self.nlp = nlp_model_loader.get_model(nlp_model)

    def replace_newlines_in_url(self, match):
        url = match.group()
        return url.replace("\n", "")

    def remove_tag_urls(self, sentence):
        url_regex = r"(?<=\])\(https?://[^\s/$.?#].[^\[\]\(\)]*(?=\))\)"
        return re.sub(url_regex, "", sentence)

    def remove_newlines_in_text(self, sentence):
        return sentence.replace("\n", " ")

    def lemmatize_text(self, sentence):
        """Function to lemmatize text data and remove the stopwords."""
        doc = self.nlp(sentence)
        # Lemmatization and removal of stop words
        processed_tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        # Return the formatted text as a string
        processed_text = " ".join(processed_tokens)
        return processed_text

    def lower_words(self, sentence):
        return sentence.lower()

    def remove_html_tags(self, sentence):
        return html2text.html2text(sentence)

    def sentence_preprocessing(self, sentence):
        sentence = self.remove_html_tags(sentence)
        sentence = self.remove_newlines_in_text(sentence)
        sentence = self.remove_tag_urls(sentence)
        sentence = self.lower_words(sentence)
        sentence = self.lemmatize_text(sentence)
        return sentence
