import os
from functools import reduce
import requests
import json
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .preprocessing import TextPreprocessor


def get_account_id(data):
    json_string = data.account.split(", 'display_name'")[0] + "}"
    json_string = json_string.replace("'", '"')
    json_string = json_string.replace("False", "false")
    json_string = json_string.replace("True", "true")
    json_object = json.loads(json_string)
    data = data.drop("account")
    return json_object["id"]


def get_account_toots(account_id):
    instance = "mastodon.hosting.medien.hs-duesseldorf.de"
    path = f"api/v1/accounts/{account_id}/statuses/"
    response = requests.get(url=f"https://{instance}/{path}")

    df = pd.DataFrame(data=response.json())
    return df["content"].to_list() if len(df) > 0 else []


def get_followed_accounts(account_id):
    instance = "mastodon.hosting.medien.hs-duesseldorf.de"
    path = f"api/v1/accounts/{account_id}/following"
    response = requests.get(url=f"https://{instance}/{path}")

    account_ids = pd.DataFrame(data=response.json()).id.to_list()
    return account_ids


def normalize(scored_sentences):
    max_score = scored_sentences[0]["cosine_sim"]
    min_score = scored_sentences[-1]["cosine_sim"]
    for index, entry in enumerate(scored_sentences):
        scored_sentences[index]["cosine_sim"] = (entry["cosine_sim"] - min_score) / (max_score - min_score)
    return scored_sentences


def get_local_recommendations_with_tfidf(account_toots, followed_toots, result_set, number_of_recommendations=10):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1)
    # Generate the tf-idf vectors for the corpus
    tfidf_matrix = tfidf_vectorizer.fit_transform(followed_toots)
    sentences_with_cosine_similarity = []
    for sentence in account_toots:
        sentence_vector = tfidf_vectorizer.transform([sentence])
        cosine_sim_sentence = linear_kernel(sentence_vector, tfidf_matrix).flatten()
        # show_scores(sentence, followed_toots, cosine_sim_sentence)

        for index, cosine_sim in enumerate(cosine_sim_sentence):
            if len(sentences_with_cosine_similarity) < index + 1:
                sentences_with_cosine_similarity.append(
                    {
                        "sentence": result_set[index],
                        "preprocessed_sentence": followed_toots[index],
                        "cosine_sim": cosine_sim,
                    }
                )
            else:
                sentences_with_cosine_similarity[index]["cosine_sim"] += cosine_sim

    sim_scores = sorted(sentences_with_cosine_similarity, key=lambda x: x["cosine_sim"], reverse=True)
    normalized_scores = normalize(sim_scores)
    return normalized_scores[:number_of_recommendations]


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


def recommend_with_tfidf_for_account(account_id, nlp_model_loader, number_of_recommendations=10):
    # get toots of user
    account_toots = get_account_toots(account_id)
    preprocessor = TextPreprocessor(nlp_model_loader)

    preprocessed_account_toots = [preprocessor.sentence_preprocessing(sentence) for sentence in account_toots]
    # get accounts followed by the user and collect relevant toots
    followed_accounts = get_followed_accounts(account_id)
    followed_toots = [get_account_toots(account_id) for account_id in followed_accounts]
    followed_toots = reduce(lambda x, y: x + y, followed_toots)
    preprocessed_followed_toots = [preprocessor.sentence_preprocessing(sentence) for sentence in followed_toots]
    recommendations = get_local_recommendations_with_tfidf(
        preprocessed_account_toots,
        preprocessed_followed_toots,
        followed_toots,
        number_of_recommendations,
    )
    return recommendations
