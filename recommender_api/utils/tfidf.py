import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

def load_test_data(filename, path):
    data = pd.read_csv(os.path.join(path, filename), sep=";")
    
    #select only english and german toots
    mask_language = (data["language"] == "en") | (data["language"] == "de")
    data = data[mask_language]
    
    return data


def recommend_with_tfidf(sentence, number_of_recommendations=10):
    
    test_toot_df = load_test_data("mastodon.social_toots.csv", "scraper/datasets")
    
    tfidf_vectorizer = TfidfVectorizer()

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