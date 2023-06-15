import spacy
import re
import html2text

# nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("de_core_news_lg")


def replace_newlines_in_url(match):
    url = match.group()
    return url.replace("\n", "")


def remove_tag_urls(sentence):
    url_regex = r"(?<=\])\(https?://[^\s/$.?#].[^\[\]\(\)]*(?=\))\)"
    return re.sub(url_regex, "", sentence)


def remove_newlines_in_text(sentence):
    return sentence.replace("\n", " ")


def lemmatize_text(sentence):
    """Function to lemmatize text data and remove the stopwords."""
    doc = nlp(sentence)
    # Lemmatization and removal of stop words
    processed_tokens = [token.lemma_ for token in doc if not token.is_stop]  # and token.is_alpha
    # Return the formatted text as a string
    processed_text = " ".join(processed_tokens)
    return processed_text


def lower_words(sentence):
    return sentence.lower()


def remove_html_tags(sentence):
    return html2text.html2text(sentence)


def sentence_preprocessing(sentence):
    sentence = remove_html_tags(sentence)
    sentence = remove_newlines_in_text(sentence)
    sentence = remove_tag_urls(sentence)
    sentence = lower_words(sentence)
    sentence = lemmatize_text(sentence)
    return sentence
