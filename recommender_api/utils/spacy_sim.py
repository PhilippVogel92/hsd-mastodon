import pandas as pd
import spacy
from sklearn.metrics.pairwise import cosine_similarity

from .preprocessing import TextPreprocessor
from recommender_api.model.mastodon_data import get_account_toots, get_followed_accounts
import numpy as np

nlp = spacy.load("de_core_news_lg")


def normalize(scored_sentences):
    max_score = scored_sentences[0]["cosine_sim"]
    min_score = scored_sentences[-1]["cosine_sim"]
    for index, entry in enumerate(scored_sentences):
        scored_sentences[index]["cosine_sim"] = (entry["cosine_sim"] - min_score) / (max_score - min_score)
    return scored_sentences


def create_word_vector(content):
    return nlp(content).vector


def create_vector_array_for_followed_toots(followed_toots_content):
    document_vectors = []
    for content in followed_toots_content:
        # compute document vector and add to document_vectors
        document_vectors.append(nlp(content).vector)
    return np.array(document_vectors)


def calculate_content_similarity_score(account_toots, followed_toots, number_of_recommendations):
    """Function to calculate the similarity score between the account toots and the toots of the followers."""
    print(account_toots)

    idx = 1
    sentence = account_toots["preprocessed_content"].iloc[idx]
    sentence_doc = nlp(account_toots["preprocessed_content"].iloc[idx])
    sentence_vector = sentence_doc.vector.reshape(1, -1)

    ##### Test ###### (activated preprocessed_content is_alpha in mastodon_data.py)
    # sentence = "# Mittelaltermarkt und Ritter."
    # sentence_doc = nlp(sentence)
    # sentence_vector = sentence_doc.vector.reshape(1, -1)

    print(sentence)
    # account_toots["vectorized_content"] = account_toots["preprocessed_content"].apply(create_word_vector)
    document_vectors = create_vector_array_for_followed_toots(followed_toots["preprocessed_content"])

    # compute similarities
    similarities = cosine_similarity(sentence_vector, document_vectors)[0]
    top_5 = np.argsort(similarities)[::-1][:10]

    for index in top_5:
        print(f"\n------ Found similarity of {similarities[index]:.3f} ------")
        print(followed_toots["preprocessed_content"].iloc[index])

    return None


def show_scores(sentence, followed_toots, cosine_sim_sentence):
    df = pd.DataFrame(cosine_sim_sentence)
    mask = df[0] > 0
    df = df[mask]
    print("----")
    print(sentence)
    for index in df.index:
        print(
            "sentence matched: ",
            followed_toots[index],
            ", cosine_sim: ",
            cosine_sim_sentence[index],
        )
    print("----")


def recommend_with_spacy_for_account(account_id, number_of_recommendations=10):
    # get toots of user
    account_toots = get_account_toots(account_id)
    preprocessor = TextPreprocessor()
    account_toots["preprocessed_content"] = account_toots["content"].apply(preprocessor.sentence_preprocessing)
    # get accounts followed by the user and collect relevant toots
    followed_accounts = get_followed_accounts(account_id)
    followed_toots = pd.DataFrame()
    # concate dataframes
    for account_id in followed_accounts:
        followed_toots = pd.concat([followed_toots, get_account_toots(account_id)])

    followed_toots["preprocessed_content"] = followed_toots["content"].apply(preprocessor.sentence_preprocessing)

    recommendations = calculate_content_similarity_score(
        account_toots,
        followed_toots,
        number_of_recommendations,
    )
    return recommendations
