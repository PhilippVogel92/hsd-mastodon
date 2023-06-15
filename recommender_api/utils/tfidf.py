import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from .preprocessing import sentence_preprocessing
from recommender_api.model.mastodon_data import get_account_toots, get_followed_accounts


def normalize(scored_sentences):
    max_score = scored_sentences[0]["cosine_sim"]
    min_score = scored_sentences[-1]["cosine_sim"]
    for index, entry in enumerate(scored_sentences):
        scored_sentences[index]["cosine_sim"] = (entry["cosine_sim"] - min_score) / (max_score - min_score)
    return scored_sentences


def get_local_recommendations_with_tfidf(account_toots, followed_toots, number_of_recommendations):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1)
    # Generate the tf-idf vectors for the corpus
    tfidf_matrix = tfidf_vectorizer.fit_transform(followed_toots["preprocessed_content"].to_list())
    sentences_with_cosine_similarity = []
    for _, account_toot in account_toots.iterrows():
        sentence_vector = tfidf_vectorizer.transform([account_toot["preprocessed_content"]])
        cosine_sim_sentence = linear_kernel(sentence_vector, tfidf_matrix).flatten()
        # show_scores(sentence, followed_toots, cosine_sim_sentence)
        for index, cosine_sim in enumerate(cosine_sim_sentence):
            if len(sentences_with_cosine_similarity) < index + 1:
                sentences_with_cosine_similarity.append(
                    {
                        "id": followed_toots.iloc[index]["id"],
                        "sentence": followed_toots.iloc[index]["content"],
                        "preprocessed_sentence": followed_toots.iloc[index]["preprocessed_content"],
                        "cosine_sim": cosine_sim,
                        "reblogs_count": float(followed_toots.iloc[index]["reblogs_count"]),
                        "favourites_count": float(followed_toots.iloc[index]["favourites_count"]),
                        "replies_count": float(followed_toots.iloc[index]["replies_count"]),
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


def recommend_with_tfidf_for_account(account_id, number_of_recommendations=10):
    # get toots of user
    account_toots = get_account_toots(account_id)
    account_toots["preprocessed_content"] = account_toots["content"].apply(sentence_preprocessing)
    # get accounts followed by the user and collect relevant toots
    followed_accounts = get_followed_accounts(account_id)
    followed_toots = pd.DataFrame()
    # concate dataframes
    for account_id in followed_accounts:
        followed_toots = pd.concat([followed_toots, get_account_toots(account_id)])

    followed_toots["preprocessed_content"] = followed_toots["content"].apply(sentence_preprocessing)

    recommendations = get_local_recommendations_with_tfidf(
        account_toots,
        followed_toots,
        number_of_recommendations,
    )
    return recommendations
