import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import requests
from functools import reduce
import html2text

def load_test_data(filename, path):
    data = pd.read_csv(os.path.join(path, filename), sep=";")
    
    #select only english and german toots
    mask_language = (data["language"] == "en") | (data["language"] == "de")
    data = data[mask_language]
    
    return data


def recommend_with_tfidf(sentence, number_of_recommendations=10):
    
    test_toot_df = load_test_data("mastodon.social_toots.csv", "scraper/datasets")
    
    tfidf_vectorizer = TfidfVectorizer(max_df=1.0, min_df=1)

    # Generate the tf-idf vectors for the corpus
    content = test_toot_df['content']
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

def recommend_with_tfidf_by_multiple(sentences, number_of_recommendations=10):
    
    test_toot_df = load_test_data("mastodon.social_toots.csv", "scraper/datasets")
    
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1)

    # Generate the tf-idf vectors for the corpus
    content = test_toot_df['content'].apply(lambda x: html2text.html2text(x))
    tfidf_matrix = tfidf_vectorizer.fit_transform(content)

    sentences_with_cosine_similarity = []
    for sentence in sentences:
        sentence_vector = tfidf_vectorizer.transform([sentence])
        cosine_sim_sentence = linear_kernel(sentence_vector, tfidf_matrix).flatten()
        #sim_scores = list(enumerate(cosine_sim_sentence)) 
        for index, cosine_sim in enumerate(cosine_sim_sentence):
            if len(sentences_with_cosine_similarity) < index + 1:
                sentences_with_cosine_similarity.append({'sentence': content.iloc[index], 'cosine_sim': cosine_sim})
            else:
                sentences_with_cosine_similarity[index]['cosine_sim'] += cosine_sim


    sim_scores = sorted(sentences_with_cosine_similarity, key=lambda x: x['cosine_sim'], reverse=True)
    return sim_scores[:number_of_recommendations]

def get_local_recommendations_with_tfidf(account_toots, followed_toots, number_of_recommendations=10):
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=1)
    # Generate the tf-idf vectors for the corpus
    tfidf_matrix = tfidf_vectorizer.fit_transform(followed_toots)
    sentences_with_cosine_similarity = []
    
    for sentence in account_toots:
        sentence_vector = tfidf_vectorizer.transform([sentence])
        cosine_sim_sentence = linear_kernel(sentence_vector, tfidf_matrix).flatten()
        #sim_scores = list(enumerate(cosine_sim_sentence)) 
        for index, cosine_sim in enumerate(cosine_sim_sentence):
            if len(sentences_with_cosine_similarity) < index + 1:
                sentences_with_cosine_similarity.append({'sentence': followed_toots[index], 'cosine_sim': cosine_sim})
            else:
                sentences_with_cosine_similarity[index]['cosine_sim'] += cosine_sim


    sim_scores = sorted(sentences_with_cosine_similarity, key=lambda x: x['cosine_sim'], reverse=True)
    return sim_scores[:number_of_recommendations]

def get_account_id(data):
    json_string = data.account.split(", \'display_name\'")[0] + "}";
    json_string = json_string.replace("'", '"')
    json_string = json_string.replace("False", "false")        
    json_string = json_string.replace("True", "true")
    json_object = json.loads(json_string)
    data = data.drop("account")
    return json_object['id']

def get_account_toots(account_id):
    instance = "mastodon.hosting.medien.hs-duesseldorf.de"
    path = f"api/v1/accounts/{account_id}/statuses/"
    response = requests.get(url = f"https://{instance}/{path}")
    
    df = pd.DataFrame(data=response.json())
    return df['content'].apply(lambda x: html2text.html2text(x)).to_list() if len(df) > 0 else []

def get_followed_accounts(account_id):
    instance = "mastodon.hosting.medien.hs-duesseldorf.de"
    path = f"api/v1/accounts/{account_id}/following"
    response = requests.get(url = f"https://{instance}/{path}")
    
    df = pd.DataFrame(data=response.json()).id.to_list()
    return df

def recommend_with_tfidf_for_account(account_id, number_of_recommendations=10):
    # get toots of user
    account_toots = get_account_toots(account_id)
    # get accounts followed by the user and collect relevant toots
    followed_accounts = get_followed_accounts(account_id)
    followed_toots = [get_account_toots(account_id) for account_id in followed_accounts]
    followed_toots = reduce(lambda x, y: x+y, followed_toots) 
    recommendations = get_local_recommendations_with_tfidf(account_toots, followed_toots, number_of_recommendations)
    return recommendations

recommend_with_tfidf_for_account(110433998616673752)