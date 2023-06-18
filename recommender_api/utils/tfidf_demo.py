import atexit
import json
import os
from functools import reduce

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from .preprocessing import sentence_preprocessing

# Load database connection parameters
load_dotenv()

# Connect to the database
conn = psycopg2.connect(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"), dbname=os.getenv("DB_NAME"),
                        user=os.getenv("DB_USER"), password=os.getenv("DB_PASS"))


def cleanup():
    """
    Close the database connection when the program is terminated.
    """
    conn.close()


# Register the cleanup function to be called when the program is terminated
atexit.register(cleanup)


def load_test_data(filename, path):
    data = pd.read_csv(os.path.join(path, filename), sep=";")

    # select only english and german toots
    mask_language = (data["language"] == "en") | (data["language"] == "de")
    data = data[mask_language]

    return data


def recommend_with_tfidf(sentence, number_of_recommendations=10):
    test_toot_df = load_test_data("mastodon.social_toots.csv", "scraper/datasets")

    tfidf_vectorizer = TfidfVectorizer(max_df=1.0, min_df=1)

    # Generate the tf-idf vectors for the corpus
    content = test_toot_df["content"]
    tfidf_matrix = tfidf_vectorizer.fit_transform(content)

    # Transform the sentence into a tf-idf vector
    sentence_vector = tfidf_vectorizer.transform([sentence])

    # Calculate the cosine similarity between the sentence vector and all toot vectors
    cosine_sim_sentence = linear_kernel(sentence_vector, tfidf_matrix).flatten()

    # Get the pairwise similarity scores
    sim_scores = list(enumerate(cosine_sim_sentence))

    # Sort the toots based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores for the specified number of most similar toots
    sim_scores = sim_scores[:number_of_recommendations]
    sim_indices = [i[0] for i in sim_scores]

    # Return the recommended toots as a list of content
    list_of_content = content.iloc[sim_indices]
    return list_of_content.tolist()


def normalize(scored_sentences):
    max_score = scored_sentences[0]["cosine_sim"]
    min_score = scored_sentences[-1]["cosine_sim"]
    for index, entry in enumerate(scored_sentences):
        scored_sentences[index]["cosine_sim"] = (entry["cosine_sim"] - min_score) / (
            max_score - min_score
        )
    return scored_sentences


def get_local_recommendations_with_tfidf(
    account_toots, followed_toots, result_set, number_of_recommendations=10
):
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

    sim_scores = sorted(
        sentences_with_cosine_similarity, key=lambda x: x["cosine_sim"], reverse=True
    )
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


def get_account_id(data):
    json_string = data.account.split(", 'display_name'")[0] + "}"
    json_string = json_string.replace("'", '"')
    json_string = json_string.replace("False", "false")
    json_string = json_string.replace("True", "true")
    json_object = json.loads(json_string)
    data.drop("account")
    return json_object["id"]


def get_account_toots(account_id):
    """
    Get all toots of an account.

    :param account_id: The id of the account.
    :return: A list of toots.
    """
    cur = conn.cursor()
    cur.execute("SELECT text FROM statuses WHERE account_id = %s;", (account_id,))
    toots = cur.fetchall()
    cur.close()
    return [toot[0] for toot in toots]


def get_followed_accounts(account_id):
    """
    Get all accounts followed by an account.

    :param account_id: The id of the account.
    :return: A list of account ids.
    """
    cur = conn.cursor()
    cur.execute("SELECT target_account_id FROM follows WHERE account_id = %s;", (account_id,))
    follows = cur.fetchall()
    cur.close()
    return [follow[0] for follow in follows]


def recommend_with_tfidf_for_account(account_id, number_of_recommendations=10):
    # get toots of user
    account_toots = get_account_toots(account_id)
    preprocesses_account_toots = [
        sentence_preprocessing(sentence) for sentence in account_toots
    ]
    # get accounts followed by the user and collect relevant toots
    followed_accounts = get_followed_accounts(account_id)
    followed_toots = [get_account_toots(account_id) for account_id in followed_accounts]
    followed_toots = reduce(lambda x, y: x + y, followed_toots)
    preprocessed_followed_toots = [
        sentence_preprocessing(sentence) for sentence in followed_toots
    ]
    recommendations = get_local_recommendations_with_tfidf(
        preprocesses_account_toots,
        preprocessed_followed_toots,
        followed_toots,
        number_of_recommendations,
    )
    return recommendations
